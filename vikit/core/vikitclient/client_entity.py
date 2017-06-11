#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: VikitClient
  Created: 06/06/17
"""

import random

from twisted.internet import reactor
from scouter.sop import FSM
from ..basic import result
from ..common import userclientop
from . import vikit_agent


########################################################################
class VikitClientConfig():
    """"""

    #----------------------------------------------------------------------
    def __init__(self, cryptor=None, ack_timeout=10,
                 retry_times=5):
        """Constructor"""
        
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
    
#
# states
#
state_START = 'start'
state_RUNNING = 'running'
state_ERROR = 'error'
state_END = 'end'

########################################################################
class VikitClient(object):
    """"""

    fsm = FSM(state_START, state_END,
              [state_END, state_RUNNING,
               state_ERROR, state_START])

    #----------------------------------------------------------------------
    def __init__(self, platform_host, platform_port, config=None):
        """"""
        #
        # config init
        #
        config = config if config else VikitClientConfig()
        self.config = config
        assert isinstance(self.config, VikitClientConfig)
        
        self.platform_host = platform_host
        self.platform_port = platform_port
        
        #
        # initial agent pool
        #
        self.agent_pool = vikit_agent.ModAgentPool(self.platform_host,
                                                   self.platform_port,
                                                   cryptor=self.config.cryptor,
                                                   ack_timeout=self.config.ack_timeout,
                                                   retry_times=self.config.retry_times)
        
    
    @fsm.transfer(state_START, state_RUNNING)
    def action_start_success(self):
        """"""
        pass
    
    @fsm.transfer(state_START, state_ERROR)
    def action_start_error(self):
        """"""
        #pass
        self.action_error_to_die()
    
    @fsm.transfer(state_RUNNING, state_END)
    def action_shutdown(self):
        """"""
        pass
    
    @fsm.transfer(state_ERROR, state_END)
    def action_error_to_die(self):
        """"""
        pass
        
    
    #----------------------------------------------------------------------
    def start(self, async=True):
        """"""
        self.agent_pool.start()
        self.action_start_success()
        
        if async:
            pass
        else:
            reactor.run()
    
    @fsm.onstate(state_RUNNING)    
    def get_modules(self):
        """"""
        raise NotImplemented()
        
    @fsm.onstate(state_RUNNING)
    def execute(self, module_name, task_id, params):
        """"""
        self.agent_pool.execute(module_name, task_id, params)