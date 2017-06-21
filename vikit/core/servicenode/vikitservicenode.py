#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Node
  Created: 06/16/17
"""

from ..actions import welcome_action, servicenode_actions, heartbeat_action
from . import vikitservice
from ..basic import vikitbase
from ..utils.singleton import Singleton
from ..launch.interfaces import LauncherIf
from ..vikitdatas import vikitservicedesc, vikitservicelauncherinfo, \
     vikitserviceinfo, healthinfo


#
# define state
#
state_WORK = 'work'
state_PENDING = 'pending'

########################################################################
class VikitServiceNode(vikitbase.VikitBase, Singleton):
    """"""
    
    

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
        
        self._sender = None
        
        #
        # state flag
        #
        self._state = state_PENDING
    
    @property
    def id(self):
        """"""
        return self._id
    
    #----------------------------------------------------------------------
    def get_sender(self):
        """"""
        return self._sender
    
    #----------------------------------------------------------------------
    def regist_sender(self, sender):
        """"""
        self._sender = sender
    
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
        sender = self.get_sender()
        
        #
        # send hearbeat
        #
        if sender:
            sender.send(hbobj)
        else:
            raise RuntimeError('sender lost (connection lost)')
        
    
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
            else:
                raise NotImplementedError()
    
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
        self.regist_sender(sender=kw.get('sender'))
    
    #----------------------------------------------------------------------
    def _on_welcomed_success(self, obj, **kw):
        """"""
        self.start_heartbeat(self.heartbeat_interval)
        self._state = state_WORK
        
        
        
            
        
    