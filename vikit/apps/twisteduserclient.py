#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: User Client
  Created: 06/24/17
"""

import time

from pprint import pprint
from scouter.sop import FSM

from twisted.internet import reactor

from ..core.vikitclient import vikitagent, vikitagentpool
from ..core.launch import twistedlaunch
from ..core.eventemitter import twistedemitter
from . import interfaces
from . import _config
from ..core.utils import getuuid, singleton
from ..core.vikitdatas import vikittaskfeedback, vikitserviceinfo

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

_NO_DESC = ['PERSISTENCE_FUNC',
            'EXPORT_FUNC',
            'INPUT_CHECK_FUNC',
            'SEARCH_FUNC']

########################################################################
class _AgentWraper(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, agent, service_timeout=30):
        """Constructor"""
        self._dict_addrs = {}
        self.service_timeout = service_timeout
        
        assert isinstance(agent, vikitagent.VikitAgent)
        self.agent = agent
    
    
    #----------------------------------------------------------------------
    def update_addr(self, service_id, addr, update_time):
        """"""
        if not self._dict_addrs.has_key(service_id):
            _ = self._dict_addrs[service_id] = {}
            
        _['addr'] = addr
        _['update_time'] = update_time
    
    #----------------------------------------------------------------------
    def shrink(self):
        """"""
        def pick_timeout_service_id(id):
            _d = self._dict_addrs.get(id)
            if _d:
                return int(self.service_timeout) > \
                       int(time.time()) - int(_d['update_time'])
            else:
                return True
        ids = filter(pick_timeout_service_id, self._dict_addrs.keys())
        
        for i in ids:
            del self._dict_addrs[i]
        
    #----------------------------------------------------------------------
    def execute(self, task_id, params):
        """"""
        self.agent.execute(task_id, params)
    

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
        raise NotImplemented()
        
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
        self.update_agentwrapper_from_services(services)
    
    #----------------------------------------------------------------------
    def build_agent(self, module_name):
        """"""
        _a = vikitagent.VikitAgent(module_name,
                                   self.config.ack_timeout,
                                   self.config.retry_times,
                                   self.config.cryptor,
                                   self.config.connect_timeout)
        _a.regist_result_callback(self.on_receive_result)
        return _a
    
    #----------------------------------------------------------------------
    def update_agentwrapper_from_services(self, service_infos):
        """"""
        for service_id, service_info in service_infos.items():
            _sinfo_obj = service_info.get('service_info')
            assert isinstance(_sinfo_obj, vikitserviceinfo.VikitServiceInfo)
            
            update_time = service_info.get('update_timestamp')
            
            #
            # addr
            #
            _port = _sinfo_obj.linfo.port
            _ip = service_info.get('ip')
            _addr = (_ip, _port)
            
            #
            # module_name
            #
            _name = _sinfo_obj.desc.module_name
            
            #
            # desc
            #
            desc = _sinfo_obj.desc.get_dict().get('mod_info')
            for i in _NO_DESC:
                if desc.has_key(i):
                    del desc[i]
            _desc = desc
            
            #
            # build agent
            #
            if not self._dict_agent.has_key(_name):
                _agent = self.build_agent(_name)
                _wraper = _AgentWraper(_agent, self.config.service_timeout)
                self._dict_agent[_name] = _wraper
            else:
                _wraper = self._dict_agent.get(_name)
                
            assert isinstance(_wraper, _AgentWraper)
            
            _wraper.update_addr(service_id, _addr, update_time)
        
        self.shrink_agentwarpper()
            
            
    #----------------------------------------------------------------------
    def shrink_agentwarpper(self):
        """"""
        for name, obj in self._dict_agent.items():
            obj.shrink()
    
    #----------------------------------------------------------------------
    def on_receive_result(self, result_obj, *v, **kw):
        """"""
        print(result_obj)
    
    #
    # active action
    #
    #----------------------------------------------------------------------
    def execute(self, module_name, params, task_id=None):
        """"""
        state = False
        
        task_id = task_id if task_id else getuuid()

        _fd = vikittaskfeedback.VikitTaskFeedback()
        
        _wrapper = self._dict_agent.get(module_name)
        _wrapper.execute(task_id, params)
    