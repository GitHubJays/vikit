#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service
  Created: 06/05/17
"""

from twisted.internet.protocol import ClientFactory

from scouter.sop import FSM

from ..common import baseprotocol, welcome
from ..basic import serializer
#from .serviceadmin_entity import VikitServiceAdmin


#
# define states
#
state_START = 'start'
state_WORKING = 'working'
state_END = 'end'

########################################################################
class PlatformClient(baseprotocol.VikitProtocol):
    """"""
    
    #fsm = FSM(state_START, state_END,
              #[state_END,
               #state_START,
               #state_WORKING])

    #----------------------------------------------------------------------
    def __init__(self, service_admin, cryptor=None, *v, **kw):
        """Constructor"""
        self._cryptor = cryptor
        baseprotocol.VikitProtocol.__init__(self, *v, **kw)
        
        #
        # service_admin
        #
        #assert isinstance(service_admin, VikitServiceAdmin)
        self.service_admin = service_admin
        
        #
        # fsm
        #
        self.fsm = FSM(state_START, state_END,
                       [state_END, state_START, state_WORKING])
        
        
    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        assert isinstance(self.serializer, serializer.Serializer)
        self.serializer.set_cryptor(self._cryptor)
    
    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        print obj
        if self.state == state_START:   
            self.service_admin.handle_welcome(obj, self)
            self.action_startup()
        else:
            self.service_admin.handle_working(obj)
        
    
    #@fsm.transfer(state_START, state_WORKING)
    def action_startup(self):
        """"""
        assert self.fsm.state == state_START
        self.fsm.state = state_WORKING
    
    #@fsm.transfer(state_WORKING, state_END)
    def action_shutdown(self):
        """"""
        assert self.fsm.state == state_WORKING
        self.fsm.state = state_END
    
    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        self.send(welcome.WelcomeBase(self.service_admin.id))
        
    @property
    def state(self):
        """"""
        return self.fsm.state
    
    
        
        
        
    
########################################################################
class PlatformClientFactory(ClientFactory):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_admin, cryptor=None, *v, **kw):
        """Constructor"""
        self.service_admin = service_admin
        self.cryptor = cryptor
        self.v = v
        self.kw = kw
        
    #----------------------------------------------------------------------
    def buildProtocol(self, addr):
        """"""
        return PlatformClient(self.service_admin, self.cryptor,
                              *self.v, **self.kw)
        
        
    
    