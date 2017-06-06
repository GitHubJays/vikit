#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service
  Created: 06/05/17
"""

from scouter.sop import FSM

from ..common import baseprotocol
from ..basic import serializer
from .serviceadmin_entity import VikitServiceAdmin


#
# define states
#
state_START
state_WORKING
state_END

########################################################################
class PlatformClient(baseprotocol.VikitProtocol):
    """"""
    
    fsm = FSM(state_START, state_END,
              [state_END,
               state_START,
               state_WORKING])

    #----------------------------------------------------------------------
    def __init__(self, service_admin, cryptor=None, *v, **kw):
        """Constructor"""
        self._cryptor = cryptor
        baseprotocol.VikitProtocol.__init__(self, *v, **kw)
        
        #
        # service_admin
        #
        assert isinstance(service_admin, VikitServiceAdmin)
        self.service_admin = service_admin
        
        
    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        assert isinstance(self.serializer, serializer.Serializer)
        self.serializer.set_cryptor(self._cryptor)
    
    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        if self.state == state_START:   
            self.service_admin.handle_welcome(obj, conn)
            self.action_startup()
        else:
            self.service_admin.handle_working(obj)
        
    
    @fsm.transfer(state_START, state_WORKING)
    def action_startup(self):
        """"""
        pass
    
    @fsm.transfer(state_WORKING, state_END)
    def action_shutdown(self):
        """"""
        pass
    
    @property
    def state(self):
        """"""
        return self.fsm.state
        
        
        
    
    