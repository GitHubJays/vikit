#!/usr/bin/env python
#coding:utf-8
"""
  Author:    --<>
  Purpose: 
  Created: 05/21/17
"""

from __future__ import unicode_literals

import os
import sys
import types
import uuid
import queue

from scouter import SDict, SList

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.internet.task import LoopingCall

from .. import mod
from . import actions
from .serializer import Serializer
from . import client

_CURRENT_PATH = os.path.dirname(__file__)
_CURRENT_MODS_PATH_R_ = '../mods/'
_CURRENT_MODS_PATH_ = os.path.join(_CURRENT_PATH, _CURRENT_MODS_PATH_R_)

########################################################################
class _TaskInServer(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id, cid):
        """Constructor"""
        self._task_id = task_id
        self._cid = cid
        
        self._STATE = client.TASK_STATE_PENDING      
    
    @property
    def task_id(self):
        """"""
        return self._task_id
    
    @property
    def cid(self):
        """"""
        return self._cid
    
    @property
    def state(self):
        """"""
        return self._STATE
    
    #----------------------------------------------------------------------
    def finish(self, result_dict):
        """"""
        self._STATE = client.TASK_STATE_FINISHED
    
    #----------------------------------------------------------------------
    def error(self):
        """"""
        self._STATE = client.TASK_STATE_ERROR
        
    
SERVICECONFIG_MOD_ATTRS = mod._MOD_ATTRS  

########################################################################
class VServiceConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, min_threads=5, max_threads=20, debug=True,
                 loop_interval=0.2, adjust_interval=3, diviation_ms=100,
                 default_mod_paths=[_CURRENT_MODS_PATH_,]):
        """Constructor"""
        
        #
        # set mod attrs
        #
        self.min_threads = min_threads
        self.max_threads = max_threads
        self.debug = debug
        self.loop_interval = loop_interval
        self.adjust_interval = adjust_interval
        self.diviation_ms = diviation_ms
        
        #
        # paths
        # 
        assert isinstance(default_mod_paths, (list, tuple))
        self.default_mod_paths = default_mod_paths
    
    @property
    def path(self):
        """"""
        return self.default_mod_paths




SERVICE_STATE_INIT = 'init'
SERVICE_STATE_WORKING = 'working'
SERVICE_STATE_ERROR = 'error'

########################################################################
class VService(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, bind_port, bind_if='',
                 config=None, cryptor=None, result_update_intervale=4,
                 ack_timeout=10, retry_times=5):
        """Constructor"""
        #
        # set STATE
        #
        self._STATE = SERVICE_STATE_INIT
        
        self._bind_port = bind_port
        self._bind_if = bind_if
        
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        
        #
        # config by VServiceConfig
        #
        self.config(config)
        assert hasattr(self, "_factory_config")
        
        #
        # cid -> conn 
        # task_id -> _TaskInService
        #
        self.CID_MAP_CONN = SDict(value={}, 
                                  new_kv_callback=self._when_new_conn_added)
        self.TASKID_MAP_TASKENTITY = SDict(value={}, 
                                           new_kv_callback=self._when_new_task_added)
        self.TASK_RESULT = SDict(value={},
                                 new_kv_callback=self._when_result_added)
        self.TASK_WAITING_ACK = SDict(value={})
        
        #
        # build mod factory
        #
        self.mod_factory = mod.ModFactory(**self._factory_config)
        
        #
        # set result trigger
        #
        self._start_collect
    
    
    #----------------------------------------------------------------------
    def config(self, config):
        """"""
        if config:
            pass
        else:
            config = VServiceConfig(min_threads=5, max_threads=20, debug=True, 
                                   loop_interval=0.2, 
                                   adjust_interval=3, 
                                   diviation_ms=100, 
                                   default_mod_paths=[_CURRENT_MODS_PATH_,])
        
        #
        # create factory config attr
        #
        self._factory_config = {}
        for i in SERVICECONFIG_MOD_ATTRS:
            self._factory_config[i] = getattr(config, i)
            
        #
        # add extra sys path
        #
        for i in config.path:
            sys.path.append(i)
    
    @property
    def state(self):
        """"""
        return self._STATE
    
    #----------------------------------------------------------------------
    def load_mod_from_module(self, module_name):
        """"""
        #
        # load module -> change state
        #
        try:
            _modobj = __import__(module_name)
        except ImportError:
            self._STATE = SERVICE_STATE_ERROR
            return False
        
        assert isinstance(_modobj, types.ModuleType)
        
        #
        # produce a mod
        #
        try:
            self._mod = self.mod_factory.build_standard_mod_from_module(_modobj)
        except Exception as e:
            #
            # load error
            #
            self._STATE = SERVICE_STATE_ERROR
            return False
        
        self._STATE = SERVICE_STATE_WORKING
        return True
    
    @property
    def mod(self):
        """"""
        if hasattr(self, '_mod'):
            return self._mod
        else:
            return None
            
    #----------------------------------------------------------------------
    def _when_new_conn_added(self, cid, conn):
        """"""
        
    #----------------------------------------------------------------------
    def _when_new_task_added(self, task_id, task_in_service_obj):
        """"""
        
    #----------------------------------------------------------------------
    def _when_result_added(self, task_id, result):
        """"""
        #
        # get _taskInServer
        #
        _task = self.TASKID_MAP_TASKENTITY.get(task_id)
        
        #
        # get conn and result
        #
        conn = self.CID_MAP_CONN.get(_task.cid)
        _result = actions.Result(task_id, dict_obj=result)
        
        #
        # add ack buffer and send result
        #
        self.wait_for_ack(task_id, _result, conn, check_timeout=self.ack_timeout)
        conn.send(_result)
    
    #----------------------------------------------------------------------
    def wait_for_ack(self, task_id, result_obj, conn, check_timeout):
        """"""
        self.TASK_WAITING_ACK[task_id] = result_obj

    #----------------------------------------------------------------------
    def ack_task(self):
        """"""
        self._ack_task(task_id)
    
    #----------------------------------------------------------------------
    def _ack_task(self, task_id):
        """"""
        if self.TASK_WAITING_ACK.has_key(task_id):
            del self.TASK_WAITING_ACK[task_id]
    
    #----------------------------------------------------------------------
    def finish_task(self, task_id):
        """"""
        self.clear_task(task_id)
    
    #----------------------------------------------------------------------
    def clear_task(self, task_id):
        """"""
        del self.TASKID_MAP_TASKENTITY[task_id]
        del self.TASK_RESULT[task_id]
        del self.TASK_WAITING_ACK[task_id]
    
    #----------------------------------------------------------------------
    def update_result(self):
        """"""
        
    
    #----------------------------------------------------------------------
    def execute(self, cid, task_id, params):
        """"""
        _mod = self.mod
        
        #
        # build _TaskInService
        #
        _t = _TaskInServer(task_id, cid)
        self.TASKID_MAP_TASKENTITY[task_id] = _t
        
        if isinstance(_mod, mod.ModStandard):
            _mod.execute(params, task_id)
        
    
    

########################################################################
class VServiceTwistedConn(Protocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vservice, cryptor=None):
        """Constructor"""
        
        assert isinstance(vservice, VService)
        self._service = vservice
        
        self._cryptor = cryptor
        self.serlzr = Serializer(self._cryptor)
        
        self.STATE = 'init'
    
    #----------------------------------------------------------------------
    def dataReceived(self, data):
        """"""
        
        obj = self.serlzr.unserialize(data)
        
        self._handler_obj(obj)    

    #----------------------------------------------------------------------
    def _handle_obj(self, obj):
        """"""
        if self.STATE == 'init':
            if isinstance(obj, actions.Welcome):
                #
                # welcome 
                #
                self.STATE = 'working'
                self._service.add_bind(obj.cid, self)

            
        if self.STATE == 'working':
            if isinstance(obj, actions.QueryTaskStatus):
                #
                # query task status
                #
                _t = self._service.get_task_status(obj.task_id)
                self.send(_t)
            elif isinstance(obj, actions.Task):
                #
                # 1. receive task
                # 2. feedback ack
                #
                self._service.execute(obj)
                task_ack_obj = self._service.get_task_ack(obj.task_id)
                self.send(task_ack_obj)
    
    
    
    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        #
        # send to peer service
        #
        text = self.serlzr.serialize(obj)
        self.transport.write(text)

########################################################################
class VServiceTwistedConnFactory(Factory):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, vserver, crypto=None):
        """"""
        self._vservice = vserver
        self._cryptor = crypto

    #----------------------------------------------------------------------
    def buildProtocol(self, addr):
        """"""
        return VServiceTwistedConn(self._vservice, self._cryptor)
    
    


########################################################################
class VServiceToPlatformTwistedClient(Protocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vservice, cryptor=None):
        """Constructor"""
        assert isinstance(vservice, VService)
        self._service = vservice
        
        self._cryptor = cryptor
        self.serlzr = Serializer(self._cryptor)
        
        self.STATE = 'init'
        
    
    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        self.send(self._service.welcome)
    
    #----------------------------------------------------------------------
    def dataReceived(self, data):
        """"""
        obj = self.serlzr.unserialize(data)
        self._handle_obj(obj)
        
    #----------------------------------------------------------------------
    def _handle_obj(self, obj):
        """"""
        if self.STATE == 'init':
            assert isinstance(obj, actions.Welcome)
            
            self.STATE = 'working'
            #
            # proce3ss welcome
            # 1. start heartbeat
            #
            self._start_heartbeat()
            
        
        if self.STATE == 'working':
            if isinstance(obj, actions.StopService):
                #
                # feed back StopServiceACK
                #
                pass
            
            if isinstance(obj, actions.HeartbeatACK):
                #
                # confirm platform running
                #
                pass
    
    #----------------------------------------------------------------------
    def _start_heartbeat(self, interval=4):
        """"""
        if not hasattr(self, 'loopcall'):
            self.loopcall = LoopingCall(self._send_heartbeat)
            self.loopcall.start(interval)
        else:
            self.loopcall.stop()
            self.loopcall.start(interval)
        
    #----------------------------------------------------------------------
    def _send_heartbeat(self):
        """"""
        hb = self._service.heartbeat
        self.send(hb)
    
    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        text = self.serlzr.serialize(obj)
        self.transport.write(text)


########################################################################
class VServiceToPlatformTwistedClientFactory(ClientFactory):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vservice, cryptor=None):
        """Constructor"""
        self._service = vservice
        self._cryptor = cryptor
    
    #----------------------------------------------------------------------
    def buildProtocol(self, addr):
        """"""
        return VServiceToPlatformTwistedClient(self._service, self._cryptor)
        
        
        
    
    
    
    
        
        
    
    