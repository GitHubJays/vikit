#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform Server
  Created: 06/02/17
"""

from scouter.sop import FSM

from twisted.internet.protocol import Factory

#from . import platform_entity
from ..common import baseprotocol
from ..basic import serializer
from ..common import welcome
from ..common import heartbeat

#
# define state
#
state_INITING = 'initing'
state_START = 'start'
state_WORKING = 'working'
state_ERROR = 'error'
state_END = 'end'

_all_states = [state_END, 
               state_ERROR,
               state_INITING,
               state_START,
               state_WORKING]

########################################################################
class PlatformProtocol(baseprotocol.VikitProtocol):
    """"""
    
    fsm = FSM(state_START, state_END,
              _all_states)

    #----------------------------------------------------------------------
    def __init__(self, platform_ins=None, cryptor=None,
                 *args, **kw):
        """Constructor"""
        #
        # 1. receive cryptor
        # 2. init protocol instance
        #
        self._cryptor = cryptor        
        baseprotocol.VikitProtocol.__init__(self, *args, **kw)
        
        #
        # bind paltform instance
        #
        self._platform = platform_ins
        #assert isinstance(self._platform, platform_entity.Platform)
        
        #
        # set FSM
        #
        self.fsm = FSM(state_START, state_END, _all_states)
        
        #
        # initial flag
        #
        self._working = False
    
    #
    # neccessary to set cryptor, even if cryptor is None
    #
    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        assert isinstance(self.serializer, serializer.Serializer)
        self.serializer.set_cryptor(self._cryptor)
        

    #   
    # core code
    #
    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        print obj
        if not self._working:
            if isinstance(obj, welcome.ServiceAdminWelcome):
                self._platform.handle_welcome(obj, self)
                #self.action_start_finish()
        else:
            self.handle_working(obj)
    
    #----------------------------------------------------------------------
    def handle_working(self, obj):
        """"""
        if isinstance(obj, heartbeat.Heartbeat):
            self._platform.handle_heartbeat(obj)
    
    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        self.send(welcome.PlatformWelcome(self._platform.id))

########################################################################
class PlatformProtocolFactory(Factory):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, platform_ins, cryptor=None):
        """Constructor"""
        self.cryptor = cryptor
        #assert isinstance(platform_ins, Platform)
        self.platform_ins = platform_ins
    
    #----------------------------------------------------------------------
    def buildProtocol(self, addr):
        """"""
        return PlatformProtocol(self.platform_ins, self.cryptor)
        
    
    