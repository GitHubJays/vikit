#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: TwistedLuancher
  Created: 06/17/17
"""

from twisted.internet import reactor
from ..interfaces import LauncherIf
from ..twistedbase import VikitTwistedProtocolFactory

########################################################################
class TwistdLauncher(LauncherIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vikit_entity):
        """Constructor"""
        #
        # init entity
        #
        self.entity = vikit_entity
        LauncherIf.__init__(self, self.entity)
        
        self.connector = None
        
        self.config = {}
    
    #----------------------------------------------------------------------
    def serve(self, port, net_if, cryptor=None, ack_timeout=10, retry_times=5):
        """"""
        #
        # add config
        #
        self.config['port'] = port
        self.config['net_if'] = net_if
        self.config['ack_timeout'] = ack_timeout
        self.config['retry_times'] = retry_times
        
        fac = VikitTwistedProtocolFactory(self.entity, 
                                          cryptor,
                                          ack_timeout, retry_times)
        self.connector = reactor.listenTCP(port, fac, interface=net_if)
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self.connector.connectionLost('user abort')
    
    #----------------------------------------------------------------------
    def get_info(self):
        """"""
        return self.config
    
    @property
    def working(self):
        """"""
        return True if self.connector else False
        
        
        
    
    