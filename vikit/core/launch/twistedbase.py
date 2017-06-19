#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Basic Protocol
  Created: 06/02/17
"""

from twisted.internet.protocol import Protocol, Factory, ClientFactory

from . import ackpool, serializer, crypto
from ..actions import welcome_action

########################################################################
class VikitTwistedProtocol(Protocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vikit_entity, cryptor=None,
                 ack_timeout=10, retry_times=5):
        """"""
        self.ack_pool = ackpool.ACKPool()
        self.serializer = serializer.Serializer(cryptor)
        
        #
        # basic attrs
        #
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        
        #
        # vikit entity
        #
        self.entity = vikit_entity

    #
    # data proccess
    #
    #----------------------------------------------------------------------
    def dataReceived(self, data):
        """"""
        #assert isinstance(self.serializer, serializer.Serializer)
        obj = self.serializer.unserialize(data)
        self.objReceived(obj)

    #----------------------------------------------------------------------
    def objReceived(self, obj):
        """"""
        #
        # just got a ack 
        #    ack and drop
        #
        if isinstance(obj, ackpool.Ack):
            #
            # ack object
            #
            self.ack_pool.ack(obj.id)
            return 
        
        #
        # got a ackable
        #    send ack and handle it
        #
        if isinstance(obj, ackpool.Ackable):
            #
            # send ack
            #
            self._send(ackpool.Ack(obj.id))        


        self.handle_obj(obj)

    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        if isinstance(obj, welcome_action.VikitWelcomeAction):
            self.id = obj.id
            self.entity.on_received_obj(obj, twisted_conn=self, from_id=self.id, sender=self)
        else:
            self.entity.on_received_obj(obj, from_id=self.id)

    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        if isinstance(obj, ackpool.Ackable):
            self.ack_pool.add(obj.id, self._send, (obj,), 
                              ack_timeout=self.ack_timeout, 
                              retry_items=self.retry_times)

        self._send(obj)


    #----------------------------------------------------------------------
    def _send(self, obj):
        """"""
        tessxt = self.serializer.serialize(obj)
        self.transport.write(tessxt)
        
        return 
    
    #----------------------------------------------------------------------
    def connectionLost(self, reason):
        """"""
        self.entity.on_connection_lost(self, reason)
    
    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        self.send(welcome_action.VikitWelcomeAction(self.entity.id))
        self.entity.on_connection_made(self)
        
        
########################################################################
class VikitTwistedProtocolFactory(Factory):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, entity, cryptor=None, ack_timeout=10, retry_times=5):
        """Constructor"""
        self.entity = entity
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
    
    #----------------------------------------------------------------------
    def buildProtocol(self, addr):
        """"""
        return VikitTwistedProtocol(self.entity, self.cryptor,
                                    self.ack_timeout,
                                    self.retry_times)

########################################################################
class VikitTwistedProtocolClientFactory(ClientFactory):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, entity, cryptor=None, ack_timeout=10,
                 retry_times=5):
        """Constructor"""
        self.entity = entity
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        
    #----------------------------------------------------------------------
    def buildProtocol(self, addr):
        """"""
        _ret = VikitTwistedProtocol(self.entity, self.cryptor,
                                    self.ack_timeout, self.retry_times)
        
        return _ret
        
        
    
    
        
    
    
