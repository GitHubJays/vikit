#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform Entity
  Created: 06/02/17
"""

from scouter.sop import FSM
from twisted.internet import reactor
 
from .platform_exc import PlatformError

from ..utils.singleton import Singleton
from ..utils import getuuid
from ..common import welcome, heartbeat, serviceadminop
#from . import platform_server
from .platform_server import PlatformProtocolFactory

#
# define state and FSM
#
state_START = 'start'
state_END = 'end'
state_WAITING = 'waiting'
state_RUNNING = 'running'
state_ERROR = 'error'

PFSM = FSM(state_START, state_END, 
           [state_END,
            state_ERROR,
            state_RUNNING,
            state_START,
            state_WAITING])

DEFAULT_PORT = 7000

########################################################################
class _ServiceAdmin(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, conn):
        """Constructor"""
        self._id = conn.id
        self._conn = conn
    
        self._running_service = {}
        self._available_services = []
        self._health_status = {}
    
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def host(self):
        """"""
        return self._conn.host
    
    #----------------------------------------------------------------------
    def start_service(self, module_name, id, port, net_if=''):
        """"""
        #raise NotImplemented()
        self._conn.send(serviceadminop.StartService(module_name, 
                                                    id, port, 
                                                    net_if))
    
    #----------------------------------------------------------------------
    def stop_service(self, id):
        """"""
        #raise NotImplemented()
        self._conn.send(serviceadminop.StopService(id))
    
    @property
    def available_services(self):
        """"""
        return self._available_services
    
    @available_services.setter
    def available_services(self, v):
        """"""
        assert isinstance(v, list)
        self._available_services = v

    @property
    def running_services(self):
        """"""
        return self._running_service
    
    @running_services.setter
    def running_services(self, v):
        """"""
        assert isinstance(v, dict)
        self._running_service = v
        
    
    #----------------------------------------------------------------------
    def service_status(self):
        """"""
        raise NotImplemented()
    
    @property
    def health_status(self):
        """"""
        return self._health_status
    
    @health_status.setter
    def health_status(self, v):
        """"""
        self._health_status = v
    
    #
    # update from heartbeat
    #
    #----------------------------------------------------------------------
    def update(self, obj):
        """"""
        assert isinstance(obj, heartbeat.Heartbeat)
        #
        # update heartbeat
        #
        self._update_service(obj.service_status)
        self._update_health_status(obj.health_status)
        
    #----------------------------------------------------------------------
    def _update_service(self, service_status):
        """"""
        self._update_available_services(service_status['available'])
        self._update_running_services(service_status['running'])
    
    #----------------------------------------------------------------------
    def _update_available_services(self, service_list):
        """"""
        self.available_services = service_list
    
    #----------------------------------------------------------------------
    def _update_running_services(self, service_dict):
        """"""
        self.running_services = service_dict
        
    #----------------------------------------------------------------------
    def _update_health_status(self, health_dict):
        """"""
        assert isinstance(health_dict, dict)
        health_dict.has_key('cpu_percent')
        health_dict.has_key('ram_percent')

    
########################################################################
class _Service:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, modname, id, admin, port, net_if=''):
        """Constructor"""
        assert isinstance(admin, _ServiceAdmin)
        self._modname = modname
        self._admin = admin
        self._port = port
        self._if = net_if
        self._id = getuuid()
    
    @property
    def id(self):
        """"""
        return self._id
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        self._admin.stop_service(self.id)
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        self._admin.start_service(self._modname, self.id, self.port, net_if)
    
    @property
    def port(self):
        """"""
        return self._port

    @port.setter
    def port(self, val):
        """"""
        self._port = val
        

########################################################################
class _ServicePool(Singleton):
    """"""
    
    _pool = {}

    #----------------------------------------------------------------------
    def __init__(self, service_admins):
        """Constructor"""
        assert isinstance(service_admins, dict)
        
        self._pool = service_admins
    
    #----------------------------------------------------------------------
    def add_service_admin(self):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def get_current_services(self):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def get_available_services(self):
        """"""
        
    #----------------------------------------------------------------------
    def _pick_up_all_exsited_service(self):
        """"""
    
    #----------------------------------------------------------------------
    def update(self, obj):
        """"""
        assert isinstance(obj, heartbeat.Heartbeat)
        
        _r = self._pool.get(obj.id)
        
        if _r:
            _r.update(obj)
    

########################################################################
class Platform(Singleton):
    """"""
    
    fsm = PFSM
    
    service_admins = {}
    service_pool = _ServicePool(service_admins)

    #----------------------------------------------------------------------
    def __init__(self, id=None, port=7000, net_if='', cryptor=None):
        """Constructor"""
        self._id = id if id else getuuid()
        self._port = port if port else DEFAULT_PORT
        self._nif = net_if if net_if else ''
        
        #
        # attrs
        #
        self.cryptor = cryptor
        
        self.factory = PlatformProtocolFactory(self, self.cryptor)
    
    @property 
    def id(self):
        """"""
        return self._id
    
    #
    # start successfully
    #
    @fsm.onstate(state_RUNNING)
    def handle_welcome(self, obj, conn):
        """"""
        if isinstance(obj, welcome.ServiceAdminWelcome):
            #
            # add admin
            #
            self._add_service_admin(obj.id, conn)
    
    @fsm.onstate(state_RUNNING)
    def handle_heartbeat(self, obj):
        """"""
        #assert isinstance(obj, heartbeat.Heartbeat)
        self._update(obj)
    
    @fsm.onstate(state_RUNNING)
    def _update(self, obj):
        """"""
        #raise NotImplemented()
        self.service_pool.update(obj)
    
    @fsm.onstate(state_RUNNING)
    def _add_service_admin(self, id, conn):
        """"""
        self.service_admins[id] = _ServiceAdmin(conn)
    
    @fsm.onstate(state_RUNNING)
    def _remove_service_admin(self, id):
        """"""
        if self.service_admins.has_key(id):
            del self.service_admins[id]
        else:
            pass
    
    @fsm.onstate(state_RUNNING)
    def start_service(self, admin_id, service_id, port, net_if=''):
        """"""
        _r = self.service_admins.get(admin_id)
        if _r:
            _r.start_service(service_id, port, net_if)
        else:
            raise PlatformError('not a vaild admin_id:{}'.format(admin_id))
    
    @fsm.onstate(state_RUNNING)
    def stop_service(self, service_id):
        """"""
        self.service_pool.stop_service(service_id)
     
   
    @fsm.onstate(state_RUNNING)
    def get_available_service(self):
        """"""
        raise NotImplemented()
    
    @fsm.onstate(state_RUNNING)
    def get_running_service(self):
        """"""
        raise NotImplemented()
        
    
    #
    # before start
    #
    @fsm.onstate(state_START)
    def serve(self):
        """"""
        reactor.listenTCP(port=self._port,
                          factory=self.factory)
        self.action_start_serve()
    
    
    #
    # define transfer
    #
    @fsm.transfer(state_START, state_WAITING)
    def action_start_serve(self):
        """"""
        self.action_finish_serve()
    
    @fsm.transfer(state_WAITING, state_RUNNING)
    def action_finish_serve(self):
        """"""
    
    @fsm.transfer(state_WAITING, state_ERROR)
    def action_starting_error(self):
        """"""
        
        self.action_shutdown()
        
    @fsm.transfer(state_RUNNING, state_ERROR)
    def action_runtime_error(self):
        """"""
        
        self.action_shutdown()
    
    @fsm.transfer(state_ERROR, state_END)
    def action_shutdown(self):
        """"""
        
        
        
    
    