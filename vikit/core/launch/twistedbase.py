#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Basic Protocol
  Created: 06/02/17
"""

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory, ClientFactory

from . import ackpool, serializer, crypto
from ..actions import welcome_action

SPLITE_CHARS = '$'
START_CHAR = '#'

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
        # set id
        #
        self.id = None
        
        self._buff = ''
        self._buff_datas = []

    #
    # data proccess
    #
    #----------------------------------------------------------------------
    def dataReceived(self, data):
        """"""
        #
        # pick for stream
        #
        #print('got data: {}'.format(data))
        state = 'pending'
        for i in data:
            #print i
            if len(self._buff):
                state = 'open'
                
            if i == START_CHAR:
                state = 'open'
                continue
                
            if i == SPLITE_CHARS:
                if state == 'open':
                    state = 'close'
                else:
                    pass
            
            if state == 'open':
                self._buff = self._buff + i
            
            if state == 'close':
                self._buff_datas.append(self._buff)
                self._buff = ''
                state = 'pending'
        
        #print self._buff_datas
        #for i in self._buff_datas:
        while True:
            i = self._buff_datas.pop()
            obj = self.serializer.unserialize(i)
            #reactor.callInThread(self.objReceived, obj)
            self.objReceived(obj)

            if self._buff_datas:
                pass
            else:
                break

    #----------------------------------------------------------------------
    def objReceived(self, obj):
        """"""
        print('[twisted] got obj: {}'.format(obj))
        #
        # just got a ack 
        #    ack and drop
        #
        if isinstance(obj, ackpool.Ack):
            #
            # ack object
            #
            self.ack_pool.ack(obj.token)
            return 
        
        #
        # got a ackable
        #    send ack and handle it
        #
        if isinstance(obj, ackpool.Ackable):
            #
            # send ack
            #
            self._send(ackpool.Ack(obj.token))        


        self.handle_obj(obj)

    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        #print('[twisted] handle obj: {}'.format(obj))
        if isinstance(obj, welcome_action.VikitWelcomeAction):
            self.id = obj.id
            self.entity.on_received_obj(obj, twisted_conn=self, from_id=self.id, sender=self)
        else:
            self.entity.on_received_obj(obj, from_id=self.id)

    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        if isinstance(obj, ackpool.Ackable):
            self.ack_pool.add(obj.token, self._send, (obj,), 
                              ack_timeout=self.ack_timeout, 
                              retry_items=self.retry_times)

        self._send(obj)


    #----------------------------------------------------------------------
    def _send(self, obj):
        """"""
        print('[twisted] send obj: {}'.format(obj))
        tessxt = self.serializer.serialize(obj)
        #print('[twisted] send raw: {}'.format(tessxt))
        tessxt = START_CHAR + tessxt + SPLITE_CHARS
        self.transport.write(tessxt)
        
        return 
    
    #----------------------------------------------------------------------
    def connectionLost(self, reason):
        """"""
        self.entity.on_connection_lost(self, reason, from_id=self.id)
    
    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        self.send(welcome_action.VikitWelcomeAction(self.entity.id))
        self.entity.on_connection_made(self, from_id=self.id, sender=self)
        
        
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
        
        
    
    
        
    
    
