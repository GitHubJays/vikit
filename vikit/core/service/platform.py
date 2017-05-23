#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform
  Created: 05/22/17
"""

from . import actions

########################################################################
class Platform(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, host, port):
        """Constructor"""
        
        self._name = name
        
        self._host = host
        self._port = port
        
    @property
    def name(self):
        """"""
        return self._name
    
    #----------------------------------------------------------------------
    def get_service(self, service_id):
        """"""
        
    #----------------------------------------------------------------------
    def show_service(self):
        """"""
    
    #----------------------------------------------------------------------
    def dump_service_status(self, service_id):
        """"""
    
    #----------------------------------------------------------------------
    def stop_service(self, service_id):
        """"""
        #
        # send stop action
        #
        actions.StopService(service_id)
    
    #----------------------------------------------------------------------
    def add_bind(self, service_id, adaptor):
        """"""
        
        pass


#
# define twisted protocal
#

from twisted.internet.protocol import Protocol, Factory

from .serializer import Serializer
from . import actions

########################################################################
class PlatformTwistedConn(Protocol):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, platform, crytor=None):
        """"""
        
        assert isinstance(platform, Platform)
        self._platform = platform
        self._cryptor = crytor
        
        self.serlzr = Serializer(self._cryptor)
        
        self.STATE = 'init'
        
    #----------------------------------------------------------------------
    def dataReceived(self, data):
        """"""
        
        obj = self.serlzr.unserialize(data)
        
        self._handler_obj(obj)
    
    #----------------------------------------------------------------------
    def _handle_obj(self, obj):
        """"""
        if self.STATE == 'init':
            if isinstance(obj, actions.Welcome):
                #
                # welcome 
                #
                self.STATE = 'working'
                self._platform.add_bind(obj.sid, self)
            
        if self.STATE == 'working':
            if isinstance(obj, actions.Hearbeat):
                #
                # update heartbeat
                #
                self._platform.update_heartbeat(obj)
            elif isinstance(obj, actions.StopServiceACK):
                #
                # receive ack for stop service
                #
                self._platform.remove_bind(obj.sid)
        
    
    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        #
        # send to peer service
        #
        text = self.serlzr.serialize(obj)
        self.transport.write(text)
    

########################################################################
class PlatformTwistedConnFactory(Factory):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, platform, cryptor=None, *vargs, **kwargs):
        """Constructor"""
        #
        # pass in attrs
        #
        self.cryptor = cryptor
        self.platform = platform
    
    #----------------------------------------------------------------------
    def buildProtocol(self):
        """"""
        return PlatformTwistedConn(self.platform, self.cryptor)
        
    
    