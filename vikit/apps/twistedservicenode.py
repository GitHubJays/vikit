#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Twisted Service Node
  Created: 06/23/17
"""

from scouter.sop import FSM
from twisted.internet import reactor

from . import interfaces
from ..core.utils import singleton
from ..core.utils import getuuid

from . import _config
from ..core.servicenode import vikitservicenode
from ..core.launch import twistedlaunch
from ..core.eventemitter import twistedemitter

ServiceNodeConfig = _config.ServiceNodeConfig

#
# define states
#
state_START = 'start'
state_CONNECTED = 'connected'
state_ERROR = 'error'
state_END = 'end'

# start -> connected
action_STARTUP = 'action_startup'
# start -> error
action_CONNECT_ERROR = 'action_error'
# connected -> error
action_RUNTIME_ERROR = 'action_runtimeerror'
# connected -> end
action_SHUTDOWN = 'action_shutdown' # normal user action
# error -> end
action_DIE = 'action_die' # unexpected action


########################################################################
class TwistedServiceNode(interfaces.AppInterfaces, singleton.Singleton):
    """"""
    
    _fsm = FSM(state_START, state_END,
               [state_CONNECTED, state_END,
                state_ERROR, state_START])
    
    _fsm.create_action(action_STARTUP, state_START, state_CONNECTED)
    _fsm.create_action(action_CONNECT_ERROR, state_START, state_ERROR)
    _fsm.create_action(action_RUNTIME_ERROR, state_CONNECTED, state_ERROR)
    _fsm.create_action(action_SHUTDOWN, state_CONNECTED, state_END)
    _fsm.create_action(action_DIE, state_ERROR, state_END)

    #----------------------------------------------------------------------
    def __init__(self, id=None, config=None):
        """Constructor"""
        #
        # basic attrs
        #
        self._id = id if id else getuuid()
        self.config = config if config else _config.ServiceNodeConfig
        
        self.servicenode_entity = vikitservicenode.VikitServiceNode(self.id, 
                                                                    self.config.heartbeat_interval)
        self.__connector = twistedlaunch.TwistdConnector(self.servicenode_entity)
        self.__emitter = twistedemitter.TwistedServiceNodeEventEmitter(self.__connector)
        
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
        return self.servicenode_entity
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        #raise NotImplemented()
        self.__connector.connect(target_host=self.config.platform_host,
                                 target_port=self.config.platform_port,
                                 cryptor=self.config.cryptor,
                                 ack_timeout=self.config.ack_timeout,
                                 retry_times=self.config.retry_times,
                                 connect_timeout=self.config.connect_timeout)
        
        self._fsm.action(action_STARTUP)
    
    #----------------------------------------------------------------------
    def shutdown(self):
        """"""
        #
        # clean the resource
        #
        self.__emitter.shutdown()
        self._fsm.action(action_SHUTDOWN)
        
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
    # active action
    #
    