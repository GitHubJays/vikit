#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ServiceNode Actions
  Created: 06/18/17
"""

from . import base
from . import ackbase

########################################################################
class StartServiceAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_id, module_name, launcher_type, launcher_config):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        self.service_id = service_id
        self.module_name = module_name
        self.launcher_type = launcher_type
        self.launcher_config = launcher_config
        
    @property
    def id(self):
        """"""
        return self.service_id


########################################################################
class StopServiceAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_id):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        
        self.service_id = service_id
        
    @property
    def id(self):
        """"""
        return self.service_id
        
    
    
        
    
    