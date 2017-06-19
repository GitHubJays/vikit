#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Twisted Connector
  Created: 06/17/17
"""

from twisted.internet import reactor
from ..interfaces import ConnecterIf
from ..twistedbase import VikitTwistedProtocolClientFactory

########################################################################
class TwistdConnector(ConnecterIf):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vikit_entity):
        """Constructor"""
        #
        # init entity
        #
        self.entity = vikit_entity
        ConnecterIf.__init__(self, self.entity)
        
        self.connector = None
        
        self.config = {}
        
    #----------------------------------------------------------------------
    def connect(self, target_host, target_port, 
                cryptor=None, ack_timeout=10, retry_times=5,
                connect_timeout=30):
        """"""
        #
        # config
        #
        self.config['target_host'] = target_host
        self.config['target_port'] = target_port
        self.config['ack_timeout'] = ack_timeout
        self.config['retry_times'] = retry_times
        self.config['connect_timeout'] = connect_timeout
        
        #
        # factory
        #
        factory = VikitTwistedProtocolClientFactory(self.entity,
                                                    cryptor,
                                                    ack_timeout,
                                                    retry_times)
        _twistedconnect = reactor.connectTCP(target_host, target_port, factory, 
                                            connect_timeout)
        
        self.connector = _twistedconnect
        
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self.connector.connectionLost('user abort')
        
    @property
    def working(self):
        """"""
        return True if self.connector else False
        
        
    
    