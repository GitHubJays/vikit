#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Result Action
  Created: 06/27/17
"""

from . import base, ackbase
from ..basic import result

########################################################################
class SubmitResultAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_id):
        """Constructor"""
        base.BaseAction.__init__(self)
        ackbase.Ackable.__init__(self)
        
        self._id = service_id
        self._dict_id_map_result = {}
    
    @property
    def id(self):
        """"""
        return self._id
    
    #----------------------------------------------------------------------
    def add(self, task_id, result_obj):
        """"""
        assert isinstance(result_obj, result.Result)
        self._dict_id_map_result[task_id] = result_obj
        
    @property
    def result_dict(self):
        """"""
        return self._dict_id_map_result


########################################################################
class AckSubmitResultAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        base.BaseAction.__init__(self)
        ackbase.Ackable.__init__(self)
        
        self._list_acked_tasks = []
        
    #----------------------------------------------------------------------
    def add(self, task_id):
        """"""
        self._list_acked_tasks.append(task_id)
        
    @property
    def task_id_list(self):
        """"""
        return self._list_acked_tasks
        

    
########################################################################
class RequireResultAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, client_id):
        """Constructor"""
        base.BaseAction.__init__(self)
        ackbase.Ackable.__init__(self)
        
        self._id = client_id
        
        self._tids = []
        
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def task_id_list(self):
        """"""
        return self._tids
    
    #----------------------------------------------------------------------
    def add(self, task_id):
        """"""
        self._tids.append(task_id)
    
    
    

########################################################################
class AckRequireResultAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        base.BaseAction.__init__(self)
        ackbase.Ackable.__init__(self)
        
        self._list_acked_tasks = []
        
    #----------------------------------------------------------------------
    def add(self, task_id):
        """"""
        self._list_acked_tasks.append(task_id)
        
    @property
    def task_id_list(self):
        """"""
        return self._list_acked_tasks
        
    
    