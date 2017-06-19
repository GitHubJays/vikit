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
    def start_heartbeat(self, interval=10):
        """"""
        if self._callback_start_heartbeat:
            self._callback_start_heartbeat(interval)
        else:
            raise NotImplementedError('not heartbeat setting, plz regist ' + \
                                      'heartbeat callback first')
    
    #----------------------------------------------------------------------
    def regist_start_heartbeat_callback(self, callback):
        """"""
        self._callback_start_heartbeat = callback
    
    #
    # core callback
    #
    #----------------------------------------------------------------------
    def on_received_obj(self, obj, *args, **kw):
        """"""
        if isinstance(obj, welcome_action.VikitWelcomeAction):
            self._on_welcomed_success()
        elif isinstance(obj, servicenode_actions.StartServiceAction):
            self.start_service(id=obj.service_id,
                               module_name=obj.module_name,
                               launcher=obj.launcher_type,
                               launcher_kw_config=obj.launcher_config)
        else:
            raise NotImplementedError()
    
    #----------------------------------------------------------------------
    def on_connection_lost(self, *v, **kw):
        """"""
        print('[!] service node connection lost')
    
    #----------------------------------------------------------------------
    def on_connection_made(self, *v, **kw):
        """"""
        print('[!] service node connection made')
    
    #----------------------------------------------------------------------
    def _on_welcomed_success(self):
        """"""
        self.start_heartbeat(self.heartbeat_interval)
        
        
            
        
    