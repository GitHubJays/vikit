#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Task Actions
  Created: 06/19/17
"""

from . import base
from . import ackbase

########################################################################
class VikitExecuteTaskAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id, params):
        """Constructor"""
        self.task_id = task_id
        self.params = params
        
    @property
    def id(self):
        """"""
        return self.task_id
        

########################################################################
class VikitResponseResultAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, result_obj):
        """Constructor"""
        
        self.result = result_obj
    
    @property    
    def id(self):
        """"""
        return self.result.get('task_id')
    
    
        
        
    
    