#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Task Feed Back
  Created: 06/22/17
"""

from . import base

########################################################################
class VikitTaskFeedback(base.VikitDatas):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, state, bind_service_id, task_id, params, reason=None):
        """Constructor"""
        #
        # execute success
        #
        self._state = state
        
        #
        # if state is False, point the reason
        #
        self._reason = ''
        
        #
        # bind service id
        #
        self.service_id = bind_service_id
        
        #
        # task attrs
        #
        self.task_id = task_id
        self.params = params
        
    @property
    def state(self):
        """"""
        return self._state
        
    
    