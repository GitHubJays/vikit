#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client For Service
  Created: 05/22/17
"""

import uuid
from scouter import SDict

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from . import actions
from . import serializer
from .. import result

TASK_STATE_FINISHED = 'finished'
TASK_STATE_TIMEOUT = 'timeout'
TASK_STATE_PENDING = 'pending'
TASK_STATE_NOT_EXISTED = 'not_exsted'
TASK_STATE_ERROR = 'error'

########################################################################
class _TaskInClient(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, task_id, params, vclient):
        """Constructor"""
        assert isinstance(vclient, VClient)
        self._vclient = vclient
        
        self._conn = self._vclient.conn
        self._cid = self._vclient.cid
        self._task_id = task_id
        
        assert isinstance(params, dict)
        self._params = params
        
        #
        # priv attrs
        #
        self._ack_flag = False
        self._retry_times = 0
        self._waitingack = False
        self._result = None
        
        #
        # loopingcall ack
        #
        self._loopingcall_ack = LoopingCall(self._checking_ack)
    
    #----------------------------------------------------------------------
    def _checking_ack(self):
        """"""
        if self.be_acked:
            self._loopingcall_ack.stop()
        else:
            if self._retry_times > self._vclient.client_config.retry_times:
                self._loopingcall_ack.stop()
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
            self._loopingcall_ack.start(self._vclient.client_config.ack_timeout)
            self._waitingack = True
    
    @property
    def cid(self):
        """"""
        return self._cid
    
    @property
    def task_id(self):
        """"""
        return self._task_id
    
    @property
    def conn(self):
        """"""
        return self._conn
    
    @property
    def params(self):
        """"""
        return self._params
    
    @property
    def task(self):
        """"""
        return actions.Task(self.cid, self.task_id, self.params)
    
    @property
    def be_acked(self):
        """"""
        return self._ack_flag
    
    #----------------------------------------------------------------------
    def ack(self):
        """"""
        self._ack_flag = True
    
    #----------------------------------------------------------------------
    def send(self):
        """"""
        assert isinstance(self._conn, VClientTwistedConn)
        
        #
        # send task to 
        #
        _t = self.task
        self._conn.send(_t)
    
    @property
    def result(self):
        """"""
        return self._result 
    
    @result.setter
    def result(self, value):
        """"""
        assert isinstance(value, dict)
        self._result = result.Result(value)
        self._conn.send(actions.ResultACK(self.task_id))
        
        
        
########################################################################
class VClientConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, crypto=None, ack_timeout=10, retry_times=5):
        """Constructor"""
        self.cryptor = crypto
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
    
    

#
# client for service
#
########################################################################
class VClient(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, rhost, rport, config=None):
        """Constructor"""
        #
        # client id (Client+uuid)
        #
        self._cid = 'Client-' + uuid.uui1().hex
        
        #
        # service port
        #
        self._rhost = rhost
        self._rport = rport
        
        #
        # config
        #
        self.client_config = config if config else VClientConfig()
        assert isinstance(self.client_config, VClientConfig)
        
        #
        # enc mod
        #
        self._cryptor = self.client_config.cryptor
        
        #
        # connection
        #
        self._connection = None
        
        #
        # task_id 2 _TaskInClient
        #
        self._dict_taskid_2_taskinclient = SDict(value={})
        
        
    @property
    def cid(self):
        """"""
        return self._cid
    
    @property
    def conn(self):
        """"""
        if self._conn:
            return self._conn
        else:
            return None
    
    #----------------------------------------------------------------------
    def connect(self, rhost=None, rport=None, crypto=None):
        """"""
        rhost = rhost if rhost else self._rhost
        rport = rport if rport else self._rport
        crypt = crypto if crypto else self._cryptor
        
        self._connection = reactor.connectTCP(host, port, )
    
    #----------------------------------------------------------------------
    def disconnect(self):
        """"""
        self._connection.connectionLost('user abort!')
    
    #----------------------------------------------------------------------
    def execute(self, params):
        """"""
        #
        # build task in client entities
        #
        _taskid = self.generator_a_task_id()
        _tic = _TaskInClient(_taskid, params, self)
        self._dict_taskid_2_taskinclient[_taskid] = _tic
        
        _tic.send()
        _tic.wait_for_ack()
        
    
    #----------------------------------------------------------------------
    def generator_a_task_id(self):
        """"""
        return uuid.uuid1().hex
    
    #----------------------------------------------------------------------
    def get_task(self, task_id):
        """"""
        return self._dict_taskid_2_taskinclient.get(task_id)
    
    #----------------------------------------------------------------------
    def receive_result(self, result):
        """"""
        if isinstance(result, actions.Result):
            result_value = result.value
        
        _t = self.get_task(result.task_id)
        assert isinstance(_t, _TaskInClient)
        _t.result = result_value
    
    #----------------------------------------------------------------------
    def ack_task(self, task_id):
        """"""
        #
        # get _TaskInClient
        #
        _t = self.get_task(task_id)
        assert isinstance(_t, _TaskInClient)
        _t.ack()
    


########################################################################
class VClientTwistedConn(Protocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, vclient, cryptor=None):
        """Constructor"""
        #
        # set vclient
        #
        assert isinstance(vclient, VClient)
        self._vclient = vclient
        
        #
        # set cryptor
        #
        self._cryptor = cryptor
        self.serlzr = serializer.Serializer(self._cryptor)
        
        #
        # set state
        #
        self.STATE = 'init'
        
    
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
            if isinstance(obj, actions.Result):
                self.handle_result(obj)
            elif isinstance(obj, actions.TaskACK):
                self.handle_TaskACK(obj)
                
    
    #----------------------------------------------------------------------
    def handle_welcome(self, obj):
        """"""
        #
        # handle welcome
        #
    
    #----------------------------------------------------------------------
    def handle_result(self, obj):
        """"""
        self._vclient.receive_result(obj)

 
    #----------------------------------------------------------------------
    def handle_TaskACK(self, obj):
        """"""
        assert isinstance(obj, actions.TaskACK)
        self._vclient.ack_task(obj.task_id)
    
    
    