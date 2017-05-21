#!/usr/bin/env python
#coding:utf-8
"""
  Author:    --<>
  Purpose: 
  Created: 05/21/17
"""

import os
import sys
import types

from . import mod

_CURRENT_PATH = os.path.dirname(__file__)
_CURRENT_MODS_PATH_R_ = '../mods/'
_CURRENT_MODS_PATH_ = os.path.join(_CURRENT_PATH, _CURRENT_MODS_PATH_R_)

########################################################################
class ServerConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, min_threads=5, max_threads=20, debug=True,
                 loop_interval=0.2, adjust_interval=3, diviation_ms=100,
                 default_mod_paths=[_CURRENT_MODS_PATH_,]):
        """Constructor"""
        
        #
        # set mod attrs
        #
        self.min_threads = min_threads
        self.max_threads = max_threads
        self.debug = debug
        self.loop_interval = loop_interval
        self.adjust_interval = adjust_interval
        self.diviation_ms = diviation_ms
        
        #
        # paths
        # 
        assert isinstance(default_mod_paths, (list, tuple))
        self.default_mod_paths = default_mod_paths


########################################################################
class Server(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, module_name, config=None):
        """Constructor"""
        
        self._module_name = module_name
        
        #
        # config
        #
        self._config = ServerConfig() if config == None else config
        assert isinstance(self._config, ServerConfig)
        
        for _path in self._config.default_mod_paths:
            sys.path.append(_path)
    
        self._module_obj = __import__(_path)
        assert isinstance(self._module_name, types.ModuleType)
        
        #
        # build mod factory
        #
        _ = {}
        for i in mod._MOD_ATTRS:
            _[i] = getattr(self._config, i)
            
        self._factory = mod.ModFactory(**_)
        
        self._mod = self._factory.build_standard_mod_from_module(self._module_obj)
        
    @property
    def mod(self):
        """"""
        return self._mod
    
    @property
    def factory(self):
        """"""
        return self._factory
    
    #----------------------------------------------------------------------
    def execute(self, params):
        """"""
        