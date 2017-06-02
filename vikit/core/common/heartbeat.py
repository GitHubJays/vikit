#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: HeartBeat
  Created: 06/02/17
"""

########################################################################
class ActionBase(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        
    
    

########################################################################
class Heartbeat(ActionBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, service_state, self_state):
        """Constructor"""
        self._id = id
        
    
    @property
    def id(self):
        """"""
        return self._id
    
    