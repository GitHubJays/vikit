#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Node
  Created: 06/16/17
"""

from ..actions import welcome_action, servicenode_actions, heartbeat_action
from ..actions import result_actions
from ..resultexchanger import TaskIdCacher, ResultCacher
from . import vikitservice
from ..basic import vikitbase, result
from ..utils.singleton import Singleton
from ..launch.interfaces import LauncherIf
from ..vikitdatas import vikitservicedesc, vikitservicelauncherinfo, \
     vikitserviceinfo, healthinfo
from ..vikitlogger import get_servicenode_logger


logger = get_servicenode_logger()

#
# define state
#
state_WORK = 'work'
state_PENDING = 'pending'

########################################################################
class VikitServiceNode(vikitbase.VikitBase, Singleton):
    """"""
    
    platform_id = None
    
    task_id_recorder = TaskIdCacher('sn_task_id_cache.db')
    result_cacher = ResultCacher('sn_result_cache.db')

    #----------------------------------------------------------------------
    def __init__(self, id, heartbeat_interval=10):
        """Constructor"""
        self._id = id
        #
        # launcher bind
        #
        self._dict_launcher = {}
        
        #
        # basic attrs
        #
        self._heartbeat_interval = heartbeat_interval
        
        #
        # private
        #
        self._callback_start_heartbeat = None
        self._callback_stop_heartbeat = None
        
        #
        # state flag
        #
        self._state = state_PENDING
    
    @property
    def id(self):
        """"""
        return self._id
    
    
    @property
    def heartbeat_interval(self):
        """"""
        return self._heartbeat_interval
    
    @heartbeat_interval.setter
    def heartbeat_interval(self, value):
        """"""
        if value == self._heartbeat_interval:
            pass
        else:
            self._heartbeat_interval = value
        
        try:
            self.start_heartbeat(self._heartbeat_interval)
        except:
            raise StandardError('cannot restart heartbeat and ' + \
                                'change interval, please reset the callback_start_heartbeat')
        
        
    
    #----------------------------------------------------------------------
    def start_service(self, id, module_name, service_config=None,
                      launcher=None, launcher_kw_config={}):
        """"""
        assert issubclass(launcher, LauncherIf), 'not a valid launcher'
        #
        # build service
        #
        vs = vikitservice.VikitService(id, service_config)
        vs.regist_result_callback(self.send_result_to_result_cacher)
        
        #
        # load mod
        #
        vs.load_mod(module_name)
        
        #
        # launcher
        #
        assert issubclass(launcher, LauncherIf)
        _launcher = launcher(vs)
        _launcher.serve(**launcher_kw_config)
    
        if not self._dict_launcher.has_key(id):
            self._dict_launcher[id] = {}
            self._dict_launcher[id]['launcher'] = _launcher
            self._dict_launcher[id]['module_name'] = module_name
        
        self._send_heartbeat()

    
    #----------------------------------------------------------------------
    def get_service_info(self, module_name=None):
        """"""
        if module_name:
            _launcher = filter(lambda x: x['module_name'] == module_name, 
                               self._dict_launcher.values())
            _launcher = map(lambda x: x['launcher'], _launcher)
        else:
            _launcher = map(lambda x: x['launcher'], self._dict_launcher.values())
        
        def _build_service_info(_lchr):
            _desc = vikitservicedesc.VikitServiceDesc(**_lchr.entity.get_info())
            _linfo = vikitservicelauncherinfo.VikitServiceLauncherInfo(**_lchr.get_info())
            return vikitserviceinfo.VikitServiceInfo(self.id, _desc, _linfo)
            
        _launcher_infos = map(_build_service_info, _launcher)
        
        return _launcher_infos
    
    #----------------------------------------------------------------------
    def get_heartbeat_obj(self):
        """"""
        return heartbeat_action.HeartBeatAction(self.id, 
                                                self.get_service_info(), None)
                                                #health_info=healthinfo.HealthInfo())
    
    #----------------------------------------------------------------------
    def shutdown_service(self, id):
        """"""
        if self._dict_launcher.has_key(id):
            _la = self._dict_launcher[id]['launcher']
            assert isinstance(_la, LauncherIf), 'not a valid launcher instance'
            _la.stop()
            
            #
            # delete launcher
            #
            del self._dict_launcher[id]
        else:
            raise StandardError('shutdown a service not existed')
    
    #----------------------------------------------------------------------
    def send_result_to_result_cacher(self, result_dict):
        """"""
        if result_dict:
            pass
        else:
            return None
        
        logger.info('[servicenode] got a result_dict: {}'.format(result_dict))
        res = result.Result(result_dict)
        task_id = result_dict.get('task_id')
        
        _submit = result_actions.SubmitResultAction(self.id)
        
        self.task_id_recorder.push_one(task_id)
        self.result_cacher.save_result(task_id, res)
        _submit.add(task_id, res)
        
        _sender = self.get_sender(self.platform_id)
        logger.info('[servicenode] preparing to send results to platform')
        if _sender:
            _sender.send(_submit)
        else:
            logger.error('[servicenode] cannot got paltform sender! cannot cache result')
    
    #
    # start / stop heartbeat
    #
    #----------------------------------------------------------------------
    def start_heartbeat(self, interval=10):
        """"""
        if self._callback_start_heartbeat:
            self._callback_start_heartbeat(interval)
        else:
            raise NotImplementedError('not heartbeat start setting, plz regist ' + \
                                      'heartbeat start callback first')
    
    #----------------------------------------------------------------------
    def stop_heartbeat(self):
        """"""
        if self._callback_stop_heartbeat:
            self._callback_stop_heartbeat()
        else:
            raise NotImplementedError('not heartbeat stop setting, plz regist ' + 
                                      'heartbeat stop callback first')
        
    
    #----------------------------------------------------------------------
    def regist_start_heartbeat_callback(self, callback):
        """"""
        assert callable(callback)
        self._callback_start_heartbeat = callback
        
    #----------------------------------------------------------------------
    def regist_stop_heartbeat_callback(self, callback):
        """"""
        assert callable(callback)
        self._callback_stop_heartbeat = callback
    
    #----------------------------------------------------------------------
    def _send_heartbeat(self):
        """"""
        hbobj = self.get_heartbeat_obj()
        
        #
        # get sender 
        #
        sender = self.get_sender(self.platform_id)
        
        #
        # send hearbeat
        #
        if sender:
            sender.send(hbobj)
            #pass
        else:
            print('sender lost (connection lost)')
        
    
    #
    # core callback
    #
    #----------------------------------------------------------------------
    def on_received_obj(self, obj, *args, **kw):
        """"""
        if self._state == state_PENDING:
            if isinstance(obj, welcome_action.VikitWelcomeAction):
                self._on_welcomed_success(obj, **kw)
            else:
                pass
        else:
            if isinstance(obj, servicenode_actions.StartServiceAction):
                self.start_service(id=obj.service_id,
                                   module_name=obj.module_name,
                                   launcher=obj.launcher_type,
                                   launcher_kw_config=obj.launcher_config)
            elif isinstance(obj, servicenode_actions.StopServiceAction):
                self.shutdown_service(id=obj.id)
            
            elif isinstance(obj, result_actions.AckSubmitResultAction):
                self.handle_ack_submit_result_action(obj)
    
    #----------------------------------------------------------------------
    def on_connection_lost(self, *v, **kw):
        """"""
        print('[servicenode] service node connection lost')
        #
        # shutdown heartbeat
        #
        print('[servicenode] stop heartbeat')
        self.stop_heartbeat()
        
        #
        # shutdown all service
        #
        print('[servicenode] shutdown all services')
        for i in self._dict_launcher.keys():
            self.shutdown_service(i)
            
        #   
        # shutdown 
        #
        
    
    #----------------------------------------------------------------------
    def on_connection_made(self, *v, **kw):
        """"""
        print('[!] service node connection made')
    
    #----------------------------------------------------------------------
    def on_received_error_action(self, obj, *v, **kw):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def _on_welcomed_success(self, obj, **kw):
        """"""
        #
        # set platform_id
        #
        self.platform_id = obj.id
        
        self.start_heartbeat(self.heartbeat_interval)
        self._state = state_WORK
    
    #----------------------------------------------------------------------
    def handle_ack_submit_result_action(self, obj):
        """"""
        assert isinstance(obj, result_actions.AckSubmitResultAction)
        
        for i in obj.task_id_list:
            self.task_id_recorder.remove_one(i)
            self.result_cacher.delete_result(i)
        
        
        
            
        
    