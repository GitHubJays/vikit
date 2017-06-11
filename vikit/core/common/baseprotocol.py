#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Basic Protocol
  Created: 06/02/17
"""

from twisted.internet.protocol import Protocol

from . import ackpool
from ..basic import serializer


########################################################################
class VikitProtocol(Protocol):
    """"""
    ack_pool = ackpool.ACKPool()
    serializer = serializer.Serializer()
    
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        self.init_cryptor()
    
    #----------------------------------------------------------------------
    def dataReceived(self, data):
        """"""
        #assert isinstance(self.serializer, serializer.Serializer)
        obj = self.serializer.unserialize(data)
        self.objReceived(obj)
    
    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def objReceived(self, obj):
        """"""
        if isinstance(obj, ackpool.Ackable):
            #
            # send ack
            #
            self._send(ackpool.Ack(obj.id))        
        
        if isinstance(obj, ackpool.Ack):
            #
            # ack object
            #
            self.ack_pool.ack(obj.id)

        else:
            self.handle_obj(obj)
    
    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def send(self, obj, ack_timeout=10, retry_times=5):
        """"""
        if isinstance(obj, ackpool.Ackable):
            self.ack_pool.add(obj.id, self._send, (obj,), 
                              ack_timeout=ack_timeout, 
                              retry_items=retry_times)
        
        self._send(obj)
    

    #----------------------------------------------------------------------
    def _send(self, obj):
        """"""
        tessxt = self.serializer.serialize(obj)
        self.transport.write(tessxt)
    