#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client Manager
  Created: 06/02/17
"""

from scouter.sop import FSM

from .singleton import Singleton
from ..core.service import VClient, VClientConfig

########################################################################
class ClientManager(Singleton):
    """"""
    
    #
    # not started
    #
    state_START = 'start'
    state_CONNECTING_PLATFORM = 'connecting_platform'
    state_FETCHED_AVAILABLE_SERVICES = 'fetched_available_services'
    state_WORKING = 'working'
    state_ERROR = 'error'
    state_TIMEOUT = 'timeout'
    state_END = 'END'
    
    fsm = FSM(state_START, state_END, [state_CONNECTING_PLATFORM,
                                       state_END,
                                       state_ERROR,
                                       state_FETCHED_AVAILABLE_SERVICES,
                                       state_START,
                                       state_TIMEOUT,
                                       state_WORKING,])

    #----------------------------------------------------------------------
    def __init__(self, platform_host, platform_port, vclient_config=None):
        """Constructor"""
        #
        # phost/pport
        #
        self._phost = platform_host
        self._pport = platform_port
    
    @fsm.transfer(state_START, state_CONNECTING_PLATFORM)
    def connect_platform(self):
        """"""
        
        
    
    