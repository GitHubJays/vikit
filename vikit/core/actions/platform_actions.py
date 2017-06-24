#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: platform
  Created: 06/21/17
"""

from . import base
from . import ackbase

########################################################################
class VikitRequestServiceListPlatform(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        base.BaseAction.__init__(self)
        
        self._client_id = id
        
    @property
    def id(self):
        """"""
        return self._client_id
    
    @property
    def from_id(self):
        """"""
        return self._client_id
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<RequestServiceList from client_id:{}>'.format(self.id)
    
########################################################################
class VikitResponseServiceListPlatform(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_info_dict):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        base.BaseAction.__init__(self)
        
        assert isinstance(service_info_dict, dict)
        self.services_dict = service_info_dict
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<ResponseServiceList from platform>'
        
    
    
        
    
    