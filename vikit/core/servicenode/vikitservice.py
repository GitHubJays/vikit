#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Vikit Service
  Created: 06/16/17
"""

import os
import types

from ..common import bases
from ..basic import result
from ..basic import mod
from ..basic import vikitbase
from ..common.vikitdatas import vikitservicedesc

##
## define state
##
#state_START = 'start'

## action: start_error INITING->ERROR
## action: runtime_error WORKING->ERROR
#state_ERROR = 'error'

## action: start START->INITING
#state_INITING = 'initing'

## action: start_finish INITING->WORKING
#state_WORKING = 'working'

## action finish WORKING->END
## action error_to_die ERROR->END
#state_END = 'end'

#_all_states = [state_END, 
               #state_ERROR,
               #state_INITING,
               #state_START,
               #state_WORKING]

#
# task_state
#
task_RUNNING = 'pending'
task_FINISHED = 'finished'


_CURRENT_PATH_ = os.path.dirname(__file__)
_CURRENT_MODS_PATH_ = os.path.join(_CURRENT_PATH_, '../../mods/')

########################################################################
class VikitServiceConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, min_threads=5, max_threads=20, debug=False,
                 loop_interval=0.2, adjust_interval=3, diviation_ms=100,
                 default_mod_paths=[_CURRENT_MODS_PATH_,]):
        """Constructor"""

        #
        # set mod/factory attrs
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
class VikitService(vikitbase.VikitBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, config=None):
        """Constructor"""
        self._id = id
        
        #
        # config
        #
        self.config = config if config else VikitServiceConfig()
        assert isinstance(self.config, VikitServiceConfig)

    
        #
        # config mod factory
        #
        self._mod_factory = mod.ModFactory(self.config.min_threads,
                                           self.config.max_threads,
                                           self.config.debug,
                                           self.config.loop_interval,
                                           self.config.adjust_interval,
                                           self.config.diviation_ms) 
        
        #
        # record task_state(running or state)
        #
        self._dict_task_state = {}
        
        #
        # result callback chains
        #
        self._list_callback_chains = []
    
    #
    # basic property
    #
    @property
    def id(self):
        """"""
        return self._id
    
    #
    # core operation functions
    #
    def load_mod(self, module_name):
        """"""
        #
        # load mod from module name
        #
        obj = __import__(module_name)
        
        assert isinstance(obj, types.ModuleType)
        self._mod = self._mod_factory.build_standard_mod_from_module(obj)
        self._mod.regist_result_callback(self.on_task_finished, False)
    
    def execute_task(self, task_id, params):
        """"""
        assert isinstance(self._mod, mod.ModStandard)
        #
        # execute by mod
        #
        self._mod.execute(params, task_id)
        self._dict_task_state[task_id] = task_RUNNING
    
    #----------------------------------------------------------------------
    def join(self):
        """"""
        self._mod.join()
    
    #----------------------------------------------------------------------
    def quit(self):
        """"""
        self._mod.close()
        
    #
    # core callback functions
    #   1. result callback
    #   2. received action obj callback
    #
    #----------------------------------------------------------------------
    def on_task_finished(self, result_obj):
        """"""
        assert isinstance(result_obj, result.Result)
        self._dict_task_state[result_obj._dict_obj['task_id']] = task_FINISHED
        
        #
        # call registed callback chains
        #
        _r = result_obj._dict_obj
        for i in self._list_callback_chains:
            if i[1]:
                try:
                    _r = i[0](_r)
                except Exception as e:
                    i[1](e)
            else:
                _r = i[0](_r)
                
        print(result_obj._dict_obj)
    
    #----------------------------------------------------------------------
    def on_received_obj(self):
        """"""
        raise NotImplemented()
    
    #
    # utils
    #
    #----------------------------------------------------------------------
    def regist_result_callback(self, callback, excption_callback=None):
        """"""
        assert callable(callback), 'not a callable obj'
        if excption_callback:
            assert callable(excption_callback), 'not a callable obj'
            
        self._list_callback_chains.append((callback, excption_callback))
        return 
        
    #----------------------------------------------------------------------
    def get_mod_info(self):
        """"""
        return self._mod.get_mod_info()
    
    #----------------------------------------------------------------------
    def get_info(self):
        """"""
        _ret = vikitservicedesc.VikitServiceDesc(id=self.id, 
                                                 mod_info=self.get_mod_info())
        return _ret.get_dict()
    
    
    