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
    
    @property
    def cid(self):
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
    def __init__(self, cid, task_id):
        """Constructor"""
        self._cid = cid
        self._task_id = task_id
    
    @property
    def cid(self):
        """"""
        return self._cid
    
    @property
    def task_id(self):
        """"""
        return self._task_id

########################################################################
class Task(ClientAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, cid, task_id, params):
        """Constructor"""
        self._cid = cid
        self._task_id = task_id
        
        assert isinstance(params, dict)
        self._params = params
        
    
    @property
    def params(self):
        """"""
        return self._params

    @property
    def task_id(self):
        """"""
        return self._task_id
    
    @property
    def cid(self):
        """"""
        return self._cid
    
########################################################################
class ResultACK(ClientAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, _id):
        """Constructor"""
        self._id = _id
    
    @property
    def task_id(self):
        """"""
        return self._id
        
    
    
        

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
    def __init__(self, _id):
        """Constructor"""
        self._id = _id
        
    @property
    def sid(self):
        """"""
        return self._id

        
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
    def __init__(self, task_id, dict_obj):
        """Constructor"""
        self._taskid = task_id
        self._dict_obj = dict_obj
        
        
    @property
    def task_id(self):
        """"""
        return self._taskid
        
        
    @property
    def value(self):
        """"""
        return self._dict_obj
        
        
# to client
########################################################################
class TaskStatus(ServiceAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id, state):
        """Constructor"""
        self._task_id = task_id
        self._state = state
    
    @property
    def task_id(self):
        """"""
        return self._task_id

########################################################################
class TaskACK(ServiceAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id):
        """Constructor"""
        self._task_id = task_id
        
    @property
    def task_id(self):
        """"""
        return self._task_id
        
    
    
    
    
    
    
    
    
    
    
    
        
    
    