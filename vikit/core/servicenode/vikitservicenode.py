#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Node
  Created: 06/16/17
"""

from . import vikitservice
from ..basic import vikitbase
from ..launch.interfaces import LauncherIf

########################################################################
class VikitServiceNode(vikitbase.VikitBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        #
        # launcher bind
        #
        self._dict_launcher = {}
    
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
            _services = filter(lambda x: x['module_name'] == module_name, 
                               self._dict_launcher.values())
            _services = map(lambda x: x['launcher'], _services)
        else:
            _services = map(lambda x: x['launcher'], self._dict_launcher.values())
        
        _service_infos = map(lambda x: x.service.get_info(), _services)
        
        return _service_infos
    
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
    def on_received_obj(self):
        """"""
        raise NotImplemented()
        
        
            
        
    