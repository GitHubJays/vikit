#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: User Client
  Created: 06/07/17
"""

from .bases import Ack, Ackable, ActionBase

from .serviceop import VikitResultInProto, VikitTaskInProto

########################################################################
class RequireInfo(Ackable, ActionBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        self._id = id
    
    @property
    def id(self):
        """"""
        return self._id

########################################################################
class ServiceInfo(Ackable, ActionBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, service_info):
        """Constructor"""
        self._id = id
        self._service_info = service_info
        
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def service_information(self):
        """"""
        return self._service_info
        
    