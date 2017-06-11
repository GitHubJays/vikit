#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ModAgent
  Created: 06/09/17
"""

import random
from scouter.sop import FSM
from twisted.internet import reactor

from ..common import userclientop, welcome
from ..utils import getuuid
from . import vikit_connector
from . import client_forplatform

########################################################################
class ModAgent(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, module_name, cryptor=None, 
                 ack_timeout=10, retry_times=5, result_callback=None):
        """Constructor"""
        #
        # basic attrs
        #
        self.module_name = module_name
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        self.result_callback = result_callback
        
        #
        # build factory
        #
        self.factory = vikit_connector.VikitServiceDriverFactory(self.cryptor,
                                                                 self.ack_timeout,
                                                                 self.retry_times,
                                                                 self.result_callback)
        
        #
        # private
        #
        self._dict_services = {}
    
    #----------------------------------------------------------------------
    def add_service(self, service_id, host, port):
        """"""
        _s = self.build_servicedriver(service_id, host, port)
        self._dict_services[service_id] = _s
    
    #----------------------------------------------------------------------
    def remove_service(self, service_id):
        """"""
        del self._dict_services[service_id]
    
    #----------------------------------------------------------------------
    def execute(self, task_id, params):
        """"""
        _s = self.select_service()
        if _s:
            assert isinstance(_s, vikit_connector.VikitServiceDriver)
            _s.execute(task_id, params)
        else:
            raise StandardError('no running service!')
    
    #----------------------------------------------------------------------
    def select_service(self):
        """"""
        if self._dict_services.values() == []:
            return None
        else:
            #
            # random select
            #
            return random.choice(self._dict_services.values())
    
    #----------------------------------------------------------------------
    def build_servicedriver(self, sid, host, port):
        """"""
        return self.factory.build_service_driver(sid, host, port)


#
# define states
#
state_START = 'start'
state_QUERYING_INFOS = 'querying'
state_WORKING = 'working'
state_TIMEOUT = 'timeout'
state_ERROR = 'error'

_all_states = [state_ERROR,
               state_QUERYING_INFOS,
               state_START,
               state_TIMEOUT,
               state_WORKING]
        
#
# 1. regist Agent
# 2. update 
#
########################################################################
class ModAgentPool(object):
    """"""
    
    fsm = FSM(state_START, state_END, 
              _all_states)

    #----------------------------------------------------------------------
    def __init__(self, platform_host, platform_port, cryptor=None, ack_timeout=10,
                 retry_times=5):
        """Constructor"""
        #
        # identifier
        #
        self.id = getuuid()
        self.platform_id = None
        self.conn = None
        
        #
        # basic attrs
        #
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        
        self.platform_host = platform_host
        self.platform_port = platform_port
         
        #
        # private fields
        #
        self._dict_modagent = {}
    
    #
    # transfer
    #
    @fsm.transfer(state_START, state_QUERYING_INFOS)
    def action_query_infos(self):
        """"""
        pass
    
    @fsm.transfer(state_QUERYING_INFOS, state_WORKING)
    def action_working(self):
        """"""
        pass
    
    @fsm.transfer(state_QUERYING_INFOS, state_TIMEOUT)
    def action_query_timeout(self):
        """"""
        self.action_error()
    
    @fsm.transfer(state_TIMEOUT, state_ERROR)
    def action_error(self):
        """"""
    
    @fsm.transfer(state_WORKING, state_END)
    def action_end(self):
        """"""
        pass
    
    @fsm.transfer(state_ERROR, state_END)
    def action_error_to_die(self):
        """"""
        pass
        
        
    #
    # private methods
    #
    #----------------------------------------------------------------------
    def _build_modagent(self, module_name):
        """"""
        return ModAgent(module_name, self.cryptor,
                        self.ack_timeout,
                        self.retry_times,
                        self.process_result)
        

    #
    # callbacks
    #
    #----------------------------------------------------------------------
    def bind_platform(self, obj):
        """"""
        assert isinstance(obj, welcome.WelcomeBase)
        
        self.platform_id = obj.id

    
    #----------------------------------------------------------------------
    def update_serviceinfo(self, obj):
        """"""
        assert isinstance(obj, userclientop.ResponseServiceInfoInProto)
        infos = obj.service_information
        for i in infos.items():
            key = i[0]
            value = i[1]
            if self._dict_modagent.has_key(key):
                raise NotImplemented()
            else:
                _ma = self._build_modagent(key)
                _ma.add_service(key, value['host'], value['port'])
                self._dict_modagent[key] = _ma
        
        self.action_working()
    
    #----------------------------------------------------------------------
    def process_result(self):
        """"""
        pass
    
    #
    # action
    #
    #----------------------------------------------------------------------
    @fsm.onstate(state_START)
    def query_serviceinfo(self):
        """"""
        self.action_query_infos()
        self.conn.send(userclientop.RequireServiceInfoInProto, 
                       self.ack_timeout,
                       self.retry_times)
        
        #self.action_query_timeout()
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        self.conn = reactor.connectTCP(self.platform_host, self.platform_port,
                                       client_forplatform.PlatformClientForUserFactory(
                                                                                      self))
        
    @fsm.onstate(state_WORKING)
    def execute(self, module_name, task_id, params):
        """"""
        _m = self._dict_modagent.get(module_name)
        if _m:
            assert isinstance(_m, ModAgent)
            _m.execute(task_id, params)
        else:
            raise StandardError('not a available module_name:{}'.format(module_name))