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
    def __init__(self, task_id, cid, vservice):
        """Constructor"""
        self._task_id = task_id
        self._cid = cid
        self._vservice = vservice
        assert isinstance(self._vservice, VService)
        self._conn = vservice.get_conn_by_cid(cid)
        
        # pri attrs
        self._result = None
        self._ack_flag = False
        self._STATE = client.TASK_STATE_PENDING
        self._retry_times = 0
        self._waitingack = False
        
        #
        # looping call to ack
        #
        self._loopingcall_ack = LoopingCall(self._checking_ack)
        
    #----------------------------------------------------------------------
    def _checking_ack(self):
        """""" 
        if self.be_acked:
            self._loopingcall_ack.stop()
            #pass
        else:
            if self._retry_times > self._vservice.service_config.ack_retry_times:
                self._loopingcall_ack.stop()
                #pass
            else:
                self._retry_times = self._retry_times + 1
                #
                # send again
                #
                self.send()
    
    #----------------------------------------------------------------------
    def wait_for_ack(self):
        """"""
        if self._waitingack:
            pass
        else:
            self._waitingack = True
            
            interval = self._vservice.service_config.ack_timeout
            self._loopingcall_ack.start(interval)
            
        
    
    @property
    def conn(self):
        """"""
        return self._conn
    
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
    
    #----------------------------------------------------------------------
    def ack(self):
        """"""
        self._ack_flag = True
    
    #----------------------------------------------------------------------
    def send(self):
        """"""
        assert isinstance(self._conn, VServiceTwistedConn)
        if isinstance(self._result, actions.Result):
            self._conn.send(self.result)
            self.wait_for_ack()
        
    
    @property
    def retry_times(self):
        """"""
        return self._retry_times
    
    @property
    def be_acked(self):
        """"""
        return self._ack_flag
    
    @property
    def result(self):
        """"""
        return self._result
    
    @result.setter
    def result(self, value):
        """"""
        assert isinstance(value, dict)
        self._result = actions.Result(self.task_id, value)
        
        
    
SERVICECONFIG_MOD_ATTRS = mod._MOD_ATTRS  

########################################################################
class VServiceConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, min_threads=5, max_threads=20, debug=True,
                 loop_interval=0.2, adjust_interval=3, diviation_ms=100,
                 default_mod_paths=[_CURRENT_MODS_PATH_,],
                 cryptor=None, result_update_interval=4, ack_timeout=10,
                 ack_retry_times=5):
        """Constructor"""
        
        #
        # set mod/factory attrs
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
        
        #
        # crytor
        #
        self.cryptor = cryptor
        
        #
        # result update interval and ack-check/retry_times attrs
        #
        self.result_update_interval = result_update_interval
        self.ack_retry_times = ack_retry_times
        self.ack_timeout = ack_timeout
        

SERVICE_STATE_INIT = 'init'
SERVICE_STATE_WORKING = 'working'
SERVICE_STATE_ERROR = 'error'

########################################################################
class VServiceAdmin(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, control_host, control_port, 
                 vservice_config=None):
        """Constructor"""
        self._name = name
        self._default_config = vservice_config if vservice_config else VServiceConfig()
        assert isinstance(self._default_config, VServiceConfig)
    
        #
        # platform entry
        #
        self._platform_client_fac = VServiceToPlatformTwistedClientFactory(self, 
                                                                           self.default_config.cryptor)
        
        #
        # running service
        #
        self._dict_running_service = SDict(value={})
        
        #
        # service/client config
        #
        self._chost = control_host
        self._cport = control_port
    
    @property
    def name(self):
        """"""
        return self._name
    
    @property
    def default_config(self):
        """"""
        return self._default_config
    
    #----------------------------------------------------------------------
    def start_new_service(self, service_name, module_name, 
                          bind_port, bind_if, config=None):
        """"""
        _config = config if config else self.default_config
        assert isinstance(_config, VServiceConfig)
        
        #
        # VService
        #
        _vs = VService(service_name, bind_port, bind_if, _config)
        _vs.load_mod(module_name)
        _vs.serve()
        _vs.working()
        
        #
        # add vservice to dict
        #
        self._dict_running_service[service_name] = _vs
        
        
        
        
        
    
    #----------------------------------------------------------------------
    def stop_service_by_name(self, name):
        """"""
        _vs = self._dict_running_service.get(name)
        if _vs:
            assert isinstance(_vs, VService)
            _vs.stop_serve()
            return True
        else:
            return Factory
    
    #----------------------------------------------------------------------
    def serve(self):
        """"""
        
        self._listened_port = reactor.connectTCP(self._chost, self._cport, 
                                                 VServiceToPlatformTwistedClientFactory(self,
                                                                                        self._default_config.cryptor))
    
    #----------------------------------------------------------------------
    def stop_serve(self):
        """"""
        if hasattr(self, '_listened_port'):
            self._listened_port.connectionLost('use abort!')
            return True
        else:
            return False
    
    @property
    def heartbeat(self):
        """"""
        return actions.Hearbeat(self.name)

    @property
    def welcome(self):
        """"""
        return actions.Welcome(self.name)
        
        
    
    
########################################################################
class VService(object):
    """
    VService -> no state working mod
    
    SERVICE_STATE_INIT: mod not loaded
    SERVICE_STATE_WORKING: mod loaded, check result and waiting ack
    SERVICE_STATE_ERROR: error when mod loading
    
    """

    #----------------------------------------------------------------------
    def __init__(self, name, bind_port, bind_if='', config=None):
        """Constructor"""
        #
        # name
        #
        self._name = name
        
        #
        # no mod loaded
        #
        self._STATE = SERVICE_STATE_INIT
        
        #
        # bind attr
        #
        self.bind_port = bind_port
        self.bind_if = bind_if
        
        #
        # config
        #
        self.service_config = VServiceConfig() if config == None else config
        assert isinstance(self.service_config, VServiceConfig)
        
        #
        # init factroy
        #
        self.mod_factory = None
        self.config_factory()
        assert isinstance(self.mod_factory, mod.ModFactory)
        
        #
        # record 1. cid to conn
        #        2. task_id to entity
        #
        self._dict_cid2conn = SDict(value={})
        self._dict_taskid2taskentity = SDict(value={})
        
        #
        # prepare 1. collect result loopingcall
        #         
        #
        self._loopingcall_collecting_result = LoopingCall(self._collecting_result)

        #
        # listend_port
        #
        self._listened_port = None
    
    #
    # property
    #
    @property
    def name(self):
        """"""
        return self._name
    
    #----------------------------------------------------------------------
    def config_factory(self):
        """"""
        #
        # extract attrs 
        #
        _ = {}
        for i in mod._MOD_ATTRS:
            _[i] = getattr(self.service_config, i)
        
        self.mod_factory = mod.ModFactory(**_)
    
    #
    # switch state
    #
    #----------------------------------------------------------------------
    def error(self):
        """"""
        self._STATE = SERVICE_STATE_ERROR
    
    #----------------------------------------------------------------------
    def working(self):
        """"""
        self._STATE = SERVICE_STATE_WORKING
        
        #
        # start loopingcall
        #
        self.start_collecing_result()
    
    #----------------------------------------------------------------------
    def quit(self):
        """"""  
        #
        # stop server
        #     
        if self._listened_port:
            self._listened_port.connectionLost('normal quit')
        
        #
        # close mod
        #
        _mod = self.mod
        assert isinstance(_mod, mod.ModStandard)
        _mod.close()
        
        # reset priv
        self._STATE = SERVICE_STATE_INIT
        self.stop_collecting_result()
        self._dict_cid2conn = SDict(value={})
        self._dict_taskid2taskentity = SDict(value={})
    
    
    #
    # op build-in dict
    #
    #----------------------------------------------------------------------
    def get_task_by_id(self, task_id):
        """"""
        return self._dict_taskid2taskentity.get(task_id)
    
    #----------------------------------------------------------------------
    def get_conn_by_cid(self, cid):
        """"""
        return self._dict_cid2conn.get(cid)
    
    #----------------------------------------------------------------------
    def add_task(self, task_entity):
        """"""
        assert isinstance(task_entity, _TaskInServer)
        self._dict_taskid2taskentity[task_entity.task_id] = task_entity
    
    #----------------------------------------------------------------------
    def bind_conn(self, cid, conn):
        """"""
        assert isinstance(conn, VServiceTwistedConn)
        self._dict_cid2conn[cid] = conn
    
    #----------------------------------------------------------------------
    def remove_conn(self, cid):
        """"""
        if self._dict_cid2conn.value.has_key(cid):
            del self._dict_cid2conn[cid]
        else:
            pass
        
    #
    # loopingcall task trigger
    #
    #----------------------------------------------------------------------
    def start_collecing_result(self):
        """"""
        
        self._loopingcall_collecting_result.start(self.service_config.result_update_interval)
    
    #----------------------------------------------------------------------
    def stop_collecting_result(self):
        """"""
        self._loopingcall_collecting_result.stop()
    
    #
    # loopingcall task core
    #
    #----------------------------------------------------------------------
    def _collecting_result(self):
        """"""
        print('collecting result!')
        _q = self.mod.result_queue
        assert isinstance(_q, queue.Queue)
        while True:
            try:
                _r = _q.get_nowait()
                print("Got Result: {}".format(_r))
            except queue.Empty:
                break
            
            _tid = _r._dict_obj.get('task_id')
            _tins = self.get_task_by_id(_tid)
            assert isinstance(_tins, _TaskInServer)
            
            _tins.result = _r._dict_obj
            _tins.send()
    
    #
    # mod 
    #
    #----------------------------------------------------------------------
    def load_mod(self, module_name):
        """"""
        _obj = None
        try:
            _obj = __import__(module_name)
        except ImportError:
            self.error()
        
        if _obj:
            self._mod = self.mod_factory.build_standard_mod_from_module(_obj)
        else:
            self._mod = None
    
    @property
    def mod(self):
        """"""
        if hasattr(self, '_mod'):
            return self._mod
        else:
            return None
    
    #
    # serve/abort
    #
    #----------------------------------------------------------------------
    def serve(self):
        """"""
        self._listened_port = reactor.listenTCP(self.bind_port, 
                                                VServiceTwistedConnFactory(self,
                                                                           self.service_config.cryptor))
    #----------------------------------------------------------------------
    def stop_serve(self):
        """"""
        self.quit()
    
    #
    # task function
    #
    #----------------------------------------------------------------------
    def execute_task(self, cid, task_id, param):
        """"""
        assert hasattr(self, '_mod'), 'vservice has to be loaded from module'
    
        #
        # add _taskInServer
        #
        _t = _TaskInServer(task_id, cid, self)
        self.add_task(_t)
        
        #
        # execute it
        #
        self._mod.execute(param, task_id)
        
        #
        # ack task
        #
        conn = self.get_conn_by_cid(cid)
        conn.send(actions.TaskACK(task_id))
        
    
    #----------------------------------------------------------------------
    def ack_result(self, task_id):
        """"""
        _t = self._dict_taskid2taskentity.get(task_id)
        if _t:
            assert isinstance(_t, _TaskInServer)
            _t.ack()
            del self._dict_taskid2taskentity[task_id]
    
    #----------------------------------------------------------------------
    def abandon_task(self, task_id):
        """"""
        self.ack_result(task_id)
        
        
    

########################################################################
class VServiceTwistedConn(Protocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vservice, cryptor=None):
        """Constructor"""
        
        self._service = vservice
        assert isinstance(vservice, VService)
        
        self._cryptor = cryptor
        self.serlzr = Serializer(self._cryptor)
        
        self.STATE = 'init'
        
        #
        # priv
        #
        self._cid = ''
    
    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        print('Made connect!')
        self.send(actions.Welcome(self._service.name))
    
    #----------------------------------------------------------------------
    def connectionLost(self, reason=''):
        """"""
        print('Lost connect: {}'.format(self._cid))
        self._service.remove_conn(self._cid)
        
    
    #----------------------------------------------------------------------
    def dataReceived(self, data):
        """"""
        
        obj = self.serlzr.unserialize(data)
        
        self._handle_obj(obj)    

    #----------------------------------------------------------------------
    def _handle_obj(self, obj):
        """"""
        if self.STATE == 'init':
            if isinstance(obj, actions.Welcome):
                self.handle_welcome(obj)
                self.STATE = 'working'
            
        if self.STATE == 'working':
            if isinstance(obj, actions.Task):
                #
                # handle task
                #
                self.handle_task(obj)
            elif isinstance(obj, actions.ResultACK):
                #
                # handle result ack
                #
                self.handle_resultACK(obj)
    
    #----------------------------------------------------------------------
    def handle_resultACK(self, obj):
        """"""
        #assert isinstance(obj, actions.ResultACK)
        self._service.ack_result(obj.task_id)
    
    #----------------------------------------------------------------------
    def handle_task(self, task_obj):
        """"""
        #assert isinstance(task_obj, actions.Task)
        
        cid = self._cid
        task_id = task_obj.task_id
        params = task_obj.params
        #assert isinstance(params, dict)
        print('Receive a task: {}, from: {}, params: {}'.format(task_id, cid, params))
        self._service.execute_task(cid, task_id, params)
        
    
    #----------------------------------------------------------------------
    def handle_welcome(self, obj):
        """"""
        #
        # process welcome 
        #
        assert isinstance(obj, actions.Welcome)
        assert obj.cid != ''
        self._service.bind_conn(obj.cid, self) 
        self._cid = obj.cid
    
    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        #
        # send to peer service
        #
        #print(obj)
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
        assert isinstance(vservice, VServiceAdmin)
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
            self.handle_welcome(obj)
            
        
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
    def handle_welcome(self, obj):
        """"""
        #
        # process welcome
        # 1. start heartbeat
        #
        self._start_heartbeat()        
    
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
        
        
        
    
    
    
    
        
        
    
    