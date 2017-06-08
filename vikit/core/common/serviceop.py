#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Op
  Created: 06/06/17
"""

from .bases import Ack, Ackable, ActionBase

########################################################################
class VikitResultInProto(Ackable, ActionBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id, result_dict):
        """Constructor"""
        self._task_id = task_id
        assert isinstance(result_dict, dict)
        self._result_dict = result_dict
    
    @property
    def id(self):
        """"""
        return self._task_id
    
    @property
    def result(self):
        """"""
        return self._result_dict

########################################################################
class VikitTaskInProto(Ackable, ActionBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id, params, client_id=None):
        """Constructor"""
        self.client_id = client_id
        self.task_id = task_id
        self._task_id = task_id
        assert isinstance(params, dict)
        self._params = params
        
    @property
    def id(self):
        """"""
        return self._task_id
    
    @property
    def params(self):
        """"""
        return self.params
        
        
    
    
        
        
    
    