#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Vikit Client
  Created: 06/16/17
"""

########################################################################
class VikitClient(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        
        self._id = id
        
        #
        # callback chains
        #
        self._list_result_callback_chains = []
        self._list_execute_callback_chains = []
        
        
    #
    # core operations
    #
    #----------------------------------------------------------------------
    def execute_task(self, task_id, params):
        """"""
        assert isinstance(params, dict)
        
        _tid, params = task_id, params
        for i in self._list_execute_callback_chains:
            if i[1]:
                try:
                    _tid, params = i[0](_tid, params)
                except Exception as e:
                    i[1](e)
            else:
                _tid, params = i[0](_tid, params)        
        
        return _tid, params
    
    
    #
    # core callbacks
    #
    #----------------------------------------------------------------------
    def on_received_obj(self, obj):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def on_received_result(self, result_dict):
        """"""
        assert isinstance(result_dict, dict)
        
        _r = result_dict
        for i in self._list_result_callback_chains:
            if i[1]:
                try:
                    _r = i[0](_r)
                except Exception as e:
                    i[1](e)
            else:
                _r = i[0](_r)        
        
        return _r
    
    #
    # utils
    #
    #----------------------------------------------------------------------
    def regist_result_callback(self, callback, exception_callback=None):
        """"""
        assert callable(callback), 'not a callable obj'
        if exception_callback:
            assert callable(exception_callback), 'not a callable obj'
            
        self._list_result_callback_chains.append((callback, exception_callback))
    
    #----------------------------------------------------------------------
    def regist_execute_callback(self, callback, exception_callback=None):
        """"""
        assert callable(callback), 'not a callable obj'
        if exception_callback:
            assert callable(exception_callback), 'not a callable obj'
            
        self._list_execute_callback_chains.append((callback, exception_callback))        

        
        
        
    
    