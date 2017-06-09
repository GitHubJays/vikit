#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Driver
  Created: 06/09/17
"""

from . import client_forservice

########################################################################
class ServiceDriver(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, host, port, client_ins, cryptor=None):
        """Constructor"""
        self.id = id
        self.host = host
        self.port = port
        
        #
        # client_ins
        #
        self._client
        
        self._flag_connected = False
    
    #----------------------------------------------------------------------
    def execute(self, ):
        """"""
        if self._flag_connected:
            self._connect()
    
    #----------------------------------------------------------------------
    def _connect(self):
        """"""
        client_forservice.ServiceClientForUserFactory(client_ins, cryptor)
        