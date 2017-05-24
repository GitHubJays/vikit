#!/usr/bin/env python
#coding:utf-8
"""
  Author:    --<>
  Purpose: 
  Created: 05/21/17
"""

import os
import sys
import types
import uuid

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


########################################################################
class VService(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, module_name, control_host, control_port, bind_port, bind_if='',
                 config=None, cryptor=None):
        """Constructor"""
        #
        # identify
        #
        self._module_name = module_name
        self._id = uuid.uuid1().hex
        
        #
        # platform ip/port
        #
        self._control_host = control_host
        self._control_port = control_port
        
        #
        # local bind port
        #
        self._interface = bind_if
        self._bind_port = bind_port
        
        #
        # cryptor
        #
        self._cryptor = cryptor
        
        #
        # config
        #
        self._config = VServiceConfig() if config == None else config
        assert isinstance(self._config, VServiceConfig)
        
        for _path in self._config.default_mod_paths:
            sys.path.append(_path)
    
        if module_name:
            self._module_obj = __import__(self._module_name)
            assert isinstance(self._module_name, types.ModuleType)
        
            #
            # build mod factory
            #
            _ = {}
            for i in mod._MOD_ATTRS:
                _[i] = getattr(self._config, i)
                
            self._factory = mod.ModFactory(**_)
            
            self._mod = self._factory.build_standard_mod_from_module(self._module_obj)
            assert isinstance(self._mod, mod.ModStandard)
        
        #
        # connection/task/waiting ack pool
        #
        self._conn_pool = {}
        self._task_pool = {}
        self._padding_pool = {}
        
        
    @property
    def mod(self):
        """"""
        return self._mod
    
    @property
    def factory(self):
        """"""
        return self._factory
    
    #----------------------------------------------------------------------
    def execute(self, params):
        """"""
        self._mod.execute(params)
        
    
    #----------------------------------------------------------------------
    def serve(self):
        """"""
        #
        # connect with platform
        #
        reactor.connectTCP(self._control_host, self._control_port,
                           VServiceToPlatformTwistedClientFactory(self, cryptor=self._cryptor))
        
        #
        # run executor
        #
        reactor.listenTCP(self._bind_port, 
                          VServiceTwistedConnFactory(self, self._cryptor),
                          interface=self._interface)
        
        #
        # reactor run!
        #
        reactor.run()
    
    #----------------------------------------------------------------------
    def stop(self):
        """"""
        reactor.stop()
    
    #
    # properties
    #
    @property
    def heartbeat(self):
        """"""
        return actions.Hearbeat(self.id)
    
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def welcome(self):
        """"""
        return actions.Welcome(self.id)

    #
    # op conn
    #
    #----------------------------------------------------------------------
    def add_bind(self, cid, conn):
        """"""
        if not self._conn_pool.has_key(cid):
            self._conn_pool[cid] = conn
        else:
            raise AssertionError('repeat client id for service:{}'.format(self.id))
        
    
    #----------------------------------------------------------------------
    def get_task_status(self, cid, task_id):
        """"""
        #
        # check conn
        #
        if self._conn_pool.has_key(cid):
            #
            # check task_id
            #
            if self._task_pool.has_key(task_id):
                #
                # retru
                #
                return actions.TaskStatus(task_id, state=client.TASK_STATE_PENDING)
        
        #
        # return None
        #
        return None
    

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
                _t = self._service.get_task_status(obj.cid, obj)
                self.send(_t)
            elif isinstance(obj, actions.Task):
                #
                # 1. receive task
                # 2. feedback ack
                #
                self._service.execute(obj)
                task_ack_obj = self._service.get_task_ack(obj.cid, obj.task_id)
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
        
        
        
    
    
    
    
        
        
    
    