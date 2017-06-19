#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define HeartBeat
  Created: 06/18/17
"""

from . import base

#from ..vikitdatas import healthinfo

########################################################################
class HeartBeatAction(base.BaseAction):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_node_id, service_infos, health_info=None):
        """Constructor"""
        self.service_node_id = service_node_id
        
        assert isinstance(service_infos, list)
        self.service_infos = service_infos

        self.health_info = health_info
        
    @property
    def id(self):
        """"""
        return self.service_node_id
        
        
    
    