#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: User Client
  Created: 06/24/17
"""

from scouter.sop import FSM

from twisted.internet import reactor

from ..core.vikitclient import vikitagent, vikitagentpool
from ..core.launch import twistedlaunch
from ..core.eventemitter import twistedemitter
from . import interfaces
from . import _config
from ..core.utils import getuuid, singleton

ClientConfig = _config.ClientConfig

#
# define states
#
state_START = 'start'
state_CONNECTED = 'connected'
state_WORKING = 'working'
state_ERROR = 'error'
state_END = 'end'

# start -> connected
action_STARTUP = 'action_startup'
# connected -> working
action_WORK = 'action_working'
# working -> end
action_SHUTDOWN = 'action_shutdown'
# connected -> error
action_CONNECTED_ERROR = 'action_error'
# error -> end
action_DIE = 'action_die'

########################################################################
class _AgentWraper(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, agent):
        """Constructor"""
    
    #----------------------------------------------------------------------
    def add_service_info(self, service_info):
        """"""
        assert isinstance()
        
        
    
    

########################################################################
class TwistedClient(interfaces.AppInterfaces, singleton.Singleton):
    """"""
    
    _fsm = FSM(state_START, state_END,
               [state_CONNECTED, state_END,
                state_ERROR, state_START, 
                state_WORKING, ])
    
    _fsm.create_action(action_STARTUP, state_START, state_CONNECTED)
    _fsm.create_action(action_WORK, state_CONNECTED, state_WORKING)
    _fsm.create_action(action_SHUTDOWN, state_WORKING, state_END)
    _fsm.create_action(action_CONNECTED_ERROR, state_START, state_ERROR)

    #----------------------------------------------------------------------
    def __init__(self, id=None, config=None):
        """Constructor"""
        self._id = id if id else getuuid()
        self.config = config if config else _config.ClientConfig()
        assert isinstance(self.config, ClientConfig)
        
        self._dict_agent = {}
        
        #
        # init agentpool
        #
        self.agentpool_entity = vikitagentpool.VikitClientAgentPool(self.id)
        self.__connector_agentpool = twistedlaunch.TwistdConnector(
                                                                  self.agentpool_entity)
        self.agentpool_emitter = twistedemitter.TwistdClientAgentPoolEmitter(self.__connector_agentpool,
                                                                             self.config.default_update_interval)
        self.agentpool_emitter.regist_on_service_update(self.on_service_update)
        
    
    @property
    def id(self):
        """"""
        return self._id
        
    @property
    def state(self):
        """"""
        return self._fsm.state
    
    @property
    def entity(self):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        #
        # start connector
        #
        self.__connector_agentpool.connect(self.config.platform_host,
                                           self.config.platform_port,
                                           self.config.cryptor,
                                           self.config.ack_timeout,
                                           self.config.retry_times,
                                           self.config.connect_timeout)

        reactor.callInThread(self._start_update_services)
        
        self._fsm.action(action_STARTUP)
    
    #----------------------------------------------------------------------
    def _start_update_services(self):
        """"""
        print('[twistedclient] starting update_services')
        while not self.agentpool_emitter.connected:
            pass
        self.agentpool_emitter.start_update_services(self.config.default_update_interval)
    
    #----------------------------------------------------------------------
    def shutdown(self):
        """"""
        #
        # clean the resource
        #
        
        
        #
        #
        #
        if reactor.running:
            reactor.stop()
    
    #----------------------------------------------------------------------
    def mainloop_start(self):
        """"""
        reactor.run()
        print('[twisted-servicenode] exit main loop!')
        
    #----------------------------------------------------------------------
    def mainloop_stop(self):
        """"""
        if not reactor.running:
            reactor.stop()

    #
    # passive 
    #
    #----------------------------------------------------------------------
    def on_service_update(self, services):
        """"""
        print(services)
        
        
        
    
    