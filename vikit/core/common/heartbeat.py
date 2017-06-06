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
    def __init__(self, id, service_status, health_status):
        """Constructor"""
        self._id = id
        
        self._service_status = service_status
        self._health_status = health_status
        
    
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def service_status(self):
        """"""
        return self._service_status
    
    @property
    def health_status(self):
        """"""
        return self._health_status
    

    
    