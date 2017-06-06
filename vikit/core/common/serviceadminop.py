#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ServiceAdmin Operations
  Created: 06/05/17
"""

from .ackpool import Ackable
from .ackpool import Ack
from .bases import ActionBase


########################################################################
class StartService(ActionBase, Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, module_name, id, port, net_if=''):
        """Constructor"""
        self.module_name = module_name
        self.id = id
        self.bind_port = port
        self.bind_if = ''
    
    @property
    def value(self):
        """"""
        return {"module_name":self.module_name,
                'id':self.id,
                'bind_port':self.bind_port,
                'bind_if':self.bind_if}

########################################################################
class StopService(ActionBase, Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        self.id = id
        
        
    
    
        
    
    