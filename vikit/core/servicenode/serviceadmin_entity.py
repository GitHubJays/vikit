#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Admin
  Created: 06/05/17
"""

import psutil

from scouter.sop import FSM
from twisted.internet import task, reactor

from ..common import heartbeat
from ..common import welcome
from ..common import serviceadminop
from .vikitservice_entity import VikitServiceConfig, VikitServiceFactory, VikitService
from .serviceadmin_client import PlatformClientFactory, PlatformClient

########################################################################
class _ServiceDesc(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, module_name, bind_port, bind_if):
        """Constructor"""
        self._id = id
        self._module_name = module_name
        self._bind_port = bind_port
        self._bind_if = bind_if
    
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def module_name(self):
        """"""
        return self._module_name
    
    @property
    def bind_port(self):
        """"""
        return self._bind_port
    
    @property
    def bind_if(self):
        """"""
        return self._bind_if
    
    @property
    def value(self):
        """"""
        _ = {'id':self.id,
             'name':self.module_name,
             'bind_port':self.bind_port,
             'bind_if':self.bind_if}
        
    
    

########################################################################
class _ServiceStatus(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, available_services, running_services):
        """Constructor"""
        self._available_services = available_services
        self._running_services = running_services
        
    @property
    def available(self):
        """"""
        return self._available_services
    
    @property
    def running(self):
        """"""
        return self._running_services
    
    @property
    def value(self):
        """"""
        _ = {'available':self.available,
             'running':self.running}
        return _
        
    
########################################################################
class _HealthStatus(object):
    """"""

    @property
    def value(self):
        """"""
        _ = {}
        _['cpu_percent'] = psutil.cpu_percent()
        _['ram_percent'] = psutil.virtual_memory().percent
        return _

########################################################################
class _Platform(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, conn):
        """Constructor"""
        self._id = id
        self.conn = conn
        
    @property
    def id(self):
        """"""
        return self._id
    
    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        self.conn.send(obj)
        
    
    

#
# define states
#
state_START = 'start'
# action: start START->INITING
state_INITING = 'initing'
# action: connect_platform INITING->CONNECT_PLATFORM
state_CONNECTING_PLATFORM = 'connect'
# action: start_finish CONNECT_PLATFORM->WORKING
state_WORKING = 'working'
# action: connect_error CONNECT_PLATFORM->ERROR
# action: runtime_error WORKING->ERROR
# action: start_error INITING->ERROR
state_ERROR = 'error'
# action: error_to_die ERROR->END
# action: shutdown WORKING->END
state_END = 'end'

_all_states = [state_CONNECTING_PLATFORM,
               state_END,
               state_ERROR,
               state_INITING,
               state_START,
               state_WORKING]


########################################################################
class VikitServiceAdmin(object):
    """"""
    
    fsm = FSM(state_START, state_END,
              _all_states)
    
    #----------------------------------------------------------------------
    def __new__(self, *v, **kw):
        """"""
        if not hasattr(self, '_instance'):
            orig = super(VikitServiceAdmin, self)
            self._instance = orig.__new__(self, *v, **kw)
        
        return self._instance
        

    #----------------------------------------------------------------------
    def __init__(self, id, platform_host, platform_port, service_config=None,
                 heartbeat_interval=10):
        """Constructor"""
        #
        # basic attrs
        #
        self._id = id
        self.platform_host = platform_host
        self.platform_port = platform_port
        self.config = service_config if service_config else VikitServiceConfig()
        assert isinstance(self.config, VikitServiceConfig)
        self.platform = None
        
        #
        # set FSM
        #
        self.action_start()
        
        #
        # service map
        #
        self._service_map = {}

        #
        # set service factory
        #
        self._service_factory = VikitServiceFactory(self.config)
        
        #
        # loopingcall heartbeat
        #
        self._heartbeat_interval = heartbeat_interval
        self._loopingcall_heartbeat = task.LoopingCall(self._send_heartbeat)
    
    @property
    def id(self):
        """"""
        return self._id
    
    @fsm.transfer(state_START, state_INITING)
    def action_start(self):
        """"""
        pass
    
    @fsm.transfer(state_INITING, state_CONNECTING_PLATFORM)
    def action_connect_platform(self):
        """"""
        #reactor.connectTCP(self.platform_host, )
    
    @fsm.transfer(state_CONNECTING_PLATFORM, state_WORKING)
    def action_start_finish(self):
        """"""
        self._start_heartbeat()
    
    @fsm.transfer(state_CONNECTING_PLATFORM, state_ERROR)
    def action_connect_error(self):
        """"""
        self.action_error_to_die()
    
    @fsm.transfer(state_WORKING, state_ERROR)
    def action_runtime_error(self):
        """"""
        #self._stop_heartbeat()
        self.action_error_to_die()
    
    @fsm.transfer(state_INITING, state_ERROR)
    def action_start_error(self):
        """"""
        self.action_error_to_die()
    
    @fsm.transfer(state_ERROR, state_END)
    def action_error_to_die(self):
        """"""
        self._stop_heartbeat()
    
    @fsm.transfer(state_WORKING, state_END)
    def action_shutdown(self):
        """"""
        self._stop_heartbeat()
    
    @fsm.onstate(state_INITING)
    def connect_paltform(self):
        """"""
        #
        # connect
        #
        self.action_connect_platform()
        
        _conn = reactor.connectTCP(self.platform_host, 
                                   self.platform_port,
                                   PlatformClientFactory(self, self.config.cryptor))
        self.bind_platform(_conn)
        self.action_start_finish()
        #raise NotImplemented()
    
    #----------------------------------------------------------------------
    def disconnect_platform(self):
        """"""
        self.platform.send(obj)
    
    @fsm.onstate(state_WORKING)
    def start_service(self, module_name, bind_port, bind_if='', config=None, id=None):
        """"""
        _service = self._service_factory.build_service_with_config(bind_port,
                                                                   bind_if,
                                                                   config,
                                                                   id)
        self.regist_service(_service)
        _service.load_mod(module_name)
        _service.serve()
    
    #----------------------------------------------------------------------
    def shutdown_service(self, id):
        """"""
        if self._service_map.has_key(id):
            _service = self._service_map[id]
            assert isinstance(_service, VikitService)
            
            #
            # VikitService
            #
            _service.shutdown()
            self.unregist_service(_service.id)
        
    
        
    #----------------------------------------------------------------------
    def regist_service(self, service_entity):
        """"""
        assert isinstance(service_entity, VikitService)
        _id = service_entity.id
        self._service_map[_id] = service_entity
    
    #----------------------------------------------------------------------
    def unregist_service(self, id):
        """"""
        if self._service_map.has_key(id):
            del self._service_map[id]
    
    @fsm.onstate(state_WORKING)
    @property
    def heartbeat(self):
        """"""
        return heartbeat.Heartbeat(self.id, 
                                   self.get_service_status(),
                                   self.get_health_status())
    
    #----------------------------------------------------------------------
    def get_service_status(self):
        """"""
        _ssts = _ServiceStatus(self.get_available_services(), 
                               running_services=self.get_running_services())
        
        return _ssts.value
        
    #----------------------------------------------------------------------
    def get_available_services(self):
        """"""
        return self._available_services

    #----------------------------------------------------------------------
    def get_running_services(self):
        """"""
        _vars = self._service_map.values()
        
        def gen_descs(i):
            assert isinstance(i, VikitService)
            bif = i._bind_if
            bport = i._bind_port
            
            _r = _ServiceDesc(i.id, i._mod.NAME,
                              bif, bport)
            
            return _r.value
                    
        return map(gen_descs, _vars)
    
    #----------------------------------------------------------------------
    def get_health_status(self):
        """"""
        _ = _HealthStatus()
        return _.value
    
    #----------------------------------------------------------------------
    @fsm.onstate(state_WORKING)
    def send_to_platform(self, obj):
        """"""
        self.platform.send(obj)
        
    @fsm.onstate(state_WORKING)
    def _send_heartbeat(self):
        """"""
        self.send_to_platform(self.heartbeat)
        
    @fsm.onstate(state_WORKING)
    def _start_heartbeat(self, interval=10):
        """"""
        #
        # update interval?
        #
        if interval == self._heartbeat_interval:
            pass
        else:
            self._stop_heartbeat()
        
        #
        # set custom interval and start with a specific interval
        # 
        interval = interval if interval else self._heartbeat_interval
        if not self._loopingcall_heartbeat.running:
            #assert isinstance(self.config, VikitServiceConfig)
            self._loopingcall_heartbeat.start(interval)
    
    @fsm.onstate(state_WORKING, state_ERROR, state_END)
    def _stop_heartbeat(self):
        """"""
        if self._loopingcall_heartbeat.running:
            self._loopingcall_heartbeat.stop()
    
    #
    # bind platform
    #
    #----------------------------------------------------------------------
    @fsm.onstate(state_CONNECTING_PLATFORM)
    def bind_platform(self, _pltfrm):
        """"""
        #assert isinstance(_pltfrm, PlatformClient)
        self.platform = _pltfrm
            
    #
    # define handle request
    #
    #----------------------------------------------------------------------
    def handle_welcome(self, obj, conn):
        """"""
        assert isinstance(obj, welcome.PlatformWelcome)
        
        #_pltfrm = _Platform(obj.id, conn)
        #self.bind_platform(_pltfrm)
        #self.action_start_finish()
    
    #----------------------------------------------------------------------
    def handle_working(self, obj):
        """"""
        if isinstance(obj, serviceadminop.StartService):
            self.start_service(**obj.value)
        
        if isinstance(obj, serviceadminop.StopService):
            self.shutdown_service(obj.id)
    
    #----------------------------------------------------------------------
    def start(self, async=True):
        """"""
        self.connect_paltform()
        
        if async:
            pass
        else:
            reactor.run()
        