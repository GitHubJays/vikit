#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Result Exchanger Ops
  Created: 06/26/17
"""

from . import base, ackbase
from ..basic import result

########################################################################
class ResultExchangerBaseAction(ackbase.Ackable, base.BaseAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        base.BaseAction.__init__(self)
        
########################################################################
class ResultExchangerSubmitAction(ResultExchangerBaseAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        ResultExchangerSubmitAction.__init__(self)
        assert isinstance(result_obj, result.Result)
        
        self._client_id = id
        self._dict_results = {}
    
    @property
    def id(self):
        """"""
        return self._client_id
    
    @property
    def task_id(self):
        """"""
        return self._task_id
    
    #----------------------------------------------------------------------
    def add_result(self, task_id, result_obj):
        """"""
        assert isinstance(result_obj, result.Result)
        if not self._dict_results.has_key(task_id):
            self._dict_results[task_id] = result_obj

    @property    
    def result_dict(self):
        """"""
        return self._dict_results
        


########################################################################
class ResultExchangerRequestAction(ResultExchangerBaseAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        ResultExchangerBaseAction.__init__(self)
        
        self._task_ids = []
    
    #----------------------------------------------------------------------
    def add_task_id(self, task_id):
        """"""
        if task_id not in self._task_ids:
            self._task_ids.append(task_id)
            
    @property
    def task_id_list(self):
        """"""
        return self._task_ids

########################################################################
class ResultExchangerReturnAction(ResultExchangerBaseAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        ResultExchangerBaseAction.__init__(self)
        self._dict_results = {}
        
    #----------------------------------------------------------------------
    def add_results(self, task_id, result_obj):
        """"""
        assert isinstance(result_obj, result.Result)
        if self._dict_results.has_key(task_id):
            pass
        else:
            self._dict_results[task_id] = result_obj
    
    @property
    def result_dict(self):
        """"""
        return self._dict_results
        
    
    
        
        
        
    
    
        
    
    