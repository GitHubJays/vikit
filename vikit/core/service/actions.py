#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Action Packet
  Created: 05/22/17
"""

#
# action base
#
########################################################################
class ActionBase(object):
    """"""

#
# common action
#
########################################################################
class Welcome(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, _id):
        """"""
        self._id = _id
    
    @property
    def sid(self):
        """"""
        return self._id
    
    @property
    def pid(self):
        """"""
        return self._id
        

#
# platform action
#
########################################################################
class PlatformAction(ActionBase):
    """"""
    
# to service
########################################################################
class HeartbeatACK(PlatformAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""


# to service
########################################################################
class StopService(PlatformAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_id):
        """Constructor"""
        self._service = service_id
    
    #----------------------------------------------------------------------
    def sid(self):
        """"""
        return self._service


#
# client query
#
########################################################################
class ClientAction(ActionBase):
    """"""

# to service    
########################################################################
class QueryTaskStatus(ClientAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id):
        """Constructor"""
        self._task_id = task_id
        
        assert isinstance(params, dict)
        self._params = params
        

#
# service action
#
########################################################################
class ServiceAction(ActionBase):
    """"""

# to platform
########################################################################
class Hearbeat(ServiceAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
# to platform
########################################################################
class StopServiceACK(ServiceAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        

# to client
########################################################################
class Result(ServiceAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
# to client
########################################################################
class TaskStatus(ServiceAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id):
        """Constructor"""
        
        
    
    
    
    
    
    
    
    
    
        
    
    