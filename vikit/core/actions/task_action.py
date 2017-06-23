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
        #ackbase.Ackable.__init__(self)
        self.token = ackbase.getuuid()
        
        self.task_id = task_id
        self.params = params
        
    @property
    def id(self):
        """"""
        return self.task_id
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<ExecuteTask task_id:{} params:{}>'.format(self.task_id, self.params)
        

########################################################################
class VikitResponseResultAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, result_obj):
        """Constructor"""
        #ackbase.Ackable.__init__(self)
        self.token = ackbase.getuuid()
        self.result = result_obj
    
    @property    
    def id(self):
        """"""
        return self.result.get('task_id')
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<TaskResult task_id:{} result:{}>'.format(self.id,
                                                          self.result)

########################################################################
class VikitRequestTaskStatus(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        self.task_id
        
    @property
    def id(self):
        """"""
        return self.task_id
    
########################################################################
class VikitResponseTaskStatus(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id, status):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        
        self.task_id = task_id
        self.status = status
    
    @property
    def id(self):
        """"""
        return self.task_id
    
    @property
    def status(self):
        """"""
        return self.status
        
        
    
    
        
        
    
    
    
    
        
        
    
    