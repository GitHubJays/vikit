#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform Server
  Created: 06/02/17
"""

from scouter.sop import FSM

from . import platform_entity
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
    
    fsm = None

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
        assert isinstance(self._platform, platform_entity.Platform)
        
        #
        # set FSM
        #
        self.fsm = FSM(state_START, state_END, _all_states)
        
        #
        # initial flag
        #
        self.action_start()
    
    #
    # neccessary to set cryptor, even if cryptor is None
    #
    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        assert isinstance(self.serializer, serializer.Serializer)
        self.serializer.set_cryptor(self._cryptor)
        
    #
    # define action for fsm
    #
    @fsm.transfer(state_START, state_INITING)
    def action_start(self):
        """"""
        pass
    
    @fsm.transfer(state_INITING, state_WORKING)
    def action_start_finish(self):
        """"""
        pass
    
    @fsm.transfer(state_WORKING, state_ERROR)
    def action_runting_error(self):
        """"""
        pass
    
    @fsm.transfer(state_INITING, state_ERROR)
    def action_starting_error(self):
        """"""
        pass
    
    @fsm.transfer(state_ERROR, state_END)
    def action_shutdown(self):
        """"""
        pass
        
    #   
    # core code
    #
    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        if isinstance(obj, welcome.ServiceAdminWelcome):
            self._platform.handle_welcome(obj, self)
            self.action_start_finish()
    
        if self.fsm.state == state_WORKING:
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

