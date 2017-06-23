#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Config
  Created: 06/23/17
"""

########################################################################
class PlatformConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, port=7000, net_interface='', ack_timeout=10, cryptor=None,
                 retry_times=5):
        """Constructor"""
        self.port = port
        self.net_interface = net_interface
        self.ack_timeout = ack_timeout
        self.cryptor = cryptor
        self.retry_times = retry_times
    
    @property
    def net_if(self):
        """"""
        return self.net_interface
        
        
    
    