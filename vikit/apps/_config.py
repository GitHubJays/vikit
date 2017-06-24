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

########################################################################
class ServiceNodeConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, platform_host, platform_port, heartbeat_interval=10,
                 ack_timeout=10, retry_times=5, connect_timeout=30,
                 cryptor=None):
        """Constructor"""
        self.platform_host = platform_host
        self.platform_port = platform_port
        
        self.heartbeat_interval = heartbeat_interval
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        self.connect_timeout = connect_timeout
        
    @property
    def target_host(self):
        """"""
        return self.platform_host
    
    @property
    def target_port(self):
        """"""
        return self.platform_port

########################################################################
class ClientConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, platform_host='127.0.0.1', platform_port=7000, heartbeat_interval=10,
                 ack_timeout=10, retry_times=5, connect_timeout=30, default_update_interval=10,
                 cryptor=None, service_timeout=30):
        """Constructor"""
        self.platform_host = platform_host
        self.platform_port = platform_port
        
        self.heartbeat_interval = heartbeat_interval
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        self.connect_timeout = connect_timeout
        self.default_update_interval = default_update_interval
        self.service_timeout = service_timeout
        
    @property
    def target_host(self):
        """"""
        return self.platform_host
    
    @property
    def target_port(self):
        """"""
        return self.platform_port
        
    
    
        
        
    
    