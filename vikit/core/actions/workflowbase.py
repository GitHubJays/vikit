#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Workflow Base
  Created: 06/26/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

from . import base, ackbase

########################################################################
class WorkflowBase(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, workflow_id, sender):
        """Constructor"""
        base.BaseAction.__init__(self)
        ackbase.Ackable.__init__(self)
        
        self._id = workflow_id
        self._sender = sender

        self.config()

    @property
    def id(self):
        """"""
        return self._id

    @property
    def sender(self):
        """"""
        return self._sender

    @abstractmethod
    def config(self):
        """"""
        pass

    #----------------------------------------------------------------------
    def action(self, action_name):
        """"""

    #----------------------------------------------------------------------
    def action_finish(self, action_name):
        """"""

    #----------------------------------------------------------------------
    def action_error(self, action_name):
        """"""

    #----------------------------------------------------------------------
    def shutdown(self):
        """"""

    @abstractmethod    
    def on_receive_workflow_action(self, obj):
        """"""
        pass

########################################################################
class WorkflowActionBase(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, workflow_id, action_name, data=None):
        """Constructor"""
        self.id = workflow_id
        self.name = action_name

        self.data = data

    @property
    def value(self):
        """"""
        return self.data

########################################################################
class WorkflowActionFinish(WorkflowActionBase):
    """"""

########################################################################
class WorkflowActionError(WorkflowActionBase):
    """"""

