#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Node
  Created: 06/16/17
"""

from ..actions import welcome_action, servicenode_actions
from . import vikitservice
from ..basic import vikitbase
from ..utils.singleton import Singleton
from ..launch.interfaces import LauncherIf
from ..vikitdatas import vikitservicedesc, vikitservicelauncherinfo, vikitserviceinfo

########################################################################
class VikitServiceNode(vikitbase.VikitBase, Singleton):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        self._id = id
        #
        # launcher bind
        #
        self._dict_launcher = {}
    
    @property
    def id(self):
        """"""
        return self._id
    
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
    def get_service_info(self, module_name):
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
    # core callback
    #
    #----------------------------------------------------------------------
    def on_received_obj(self, obj, *args, **kw):
        """"""
        if isinstance(obj, welcome_action.VikitWelcomeAction):
            #raise StandardError()
            pass
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
        pass
    
    #----------------------------------------------------------------------
    def on_connection_made(self, *v, **kw):
        """"""
        pass
        
        
            
        
    