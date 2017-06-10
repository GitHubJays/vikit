#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Driver
  Created: 06/09/17
"""

from twisted.internet import reactor
from scouter.sop import FSM

from . import client_forservice
from ..common import userclientop
from ..basic import result
from ..utils import getuuid


########################################################################
class _Task(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, params, client_id, result_callback=None):
        """Constructor"""
        self.id = id
        self.params = params
        self.client_id = client_id
        
        #
        # callback
        #
        self._result_callback = result_callback
         
        #
        # priv
        #
        self._result = None
        
    #----------------------------------------------------------------------
    def finish(self, result_dict):
        """"""
        self._result = result.Result(result_dict)
        
        #
        # callback
        #
        if self._result_callback:
            self._result_callback(result_dict, self.id, \
                                  self.params, self.client_id)
    
    @property
    def result(self):
        """"""
        return self._result


#
# define state
#
state_START = 'start'
# action: connect START->CONNECTED
state_CONNECTED = 'connected'
# action: connect_timeout START->TIMEOUT
# action: running_timeout CONNECTED->TIMEOUT
state_TIMEOUT = 'timeout'
# action: shutdown CONNECTED->END
# action: timeout_to_die TIMEOUT->END
state_END = 'end'

########################################################################
class VikitServiceDriver(object):
    """"""
    
    fsm = FSM(state_START, state_END,
              [state_CONNECTED,
               state_END,
               state_START,
               state_TIMEOUT])

    #----------------------------------------------------------------------
    def __init__(self, id, host, port, cryptor=None,
                 ack_timeout=10, retry_timeout=5, result_callback=None):
        """Constructor"""
        self.id = id
        self.host = host
        self.port = port
        
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_timeout
        
        #
        # callback()
        #
        assert callable(result_callback) or result_callback == None
        self._result_callback = result_callback
        
        #
        # priv attrs
        #
        self._connector = None
        self._dict_tasks = {}
    
    @fsm.transfer(state_START, state_CONNECTED)
    def action_connect(self):
        """"""
        assert isinstance(self._connector, client_forservice.ServiceClientForUser)
    
    @fsm.transfer(state_START, state_TIMEOUT)
    def action_connect_timeout(self):
        """"""
        pass
    
    @fsm.transfer(state_CONNECTED, state_TIMEOUT)
    def action_running_timeout(self):
        """"""
        pass
    
    @fsm.transfer(state_CONNECTED, state_END)
    def action_shutdown(self):
        """"""
        pass
    
    @fsm.transfer(state_TIMEOUT, state_END)
    def action_timeout_to_die(self):
        """"""
        pass
        

    
    #
    # behaviors
    #
    #----------------------------------------------------------------------
    def connect(self):
        """"""
        self._connector = reactor.connectTCP(self.host, self.port,
                                             client_forservice.\
                                             ServiceClientForUserFactory(self,
                                                                         self.cryptor))
        
        self.action_connect()
    
    #----------------------------------------------------------------------
    def execute(self, task_id, params):
        """"""
        if self.fsm.state == state_START:
            self.connect()
        
        assert isinstance(params, dict)
        
        #
        # build/add(regist) task
        #
        _t = userclientop.VikitTaskInProto(task_id, params, 
                                           self._connector.id)
        self.regist_task(_t)
        self._connector.send(obj=_t, ack_timeout=self.ack_timeout,
                             retry_times=self.retry_times)

    #----------------------------------------------------------------------
    def regist_task(self, task_obj):
        """"""
        assert isinstance(task_obj, userclientop.VikitTaskInProto)
        
        #
        # build _Task obj
        #
        _tsk = _Task(task_obj.id, task_obj.params,
                     task_obj.client_id,
                     result_callback=self._result_callback)
        self._dict_tasks[_tsk.id] = _tsk
    
    #----------------------------------------------------------------------
    def unregist_task(self, task_id=None):
        """"""
        _tsk = None
        
        if self._dict_tasks.has_key(task_id):
            _tsk = self._dict_tasks.get(task_id)
            del self._dict_tasks[task_id]
        
        return _tsk
    
    #----------------------------------------------------------------------
    def callback_finish_task(self, obj):
        """"""
        assert isinstance(obj, userclientop.VikitResultInProto)
        
        tsk_id = obj._task_id
        
        _tskins = self._dict_tasks.get(tsk_id)
        if _tskins:
            assert isinstance(_tskins, _Task)
            _tskins.finish(obj.result)
        
        
        
########################################################################
class VikitServiceDriverFactory(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, cryptor=None, ack_timeout=10, 
                 retry_times=5, result_callback=None):
        """Constructor"""
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        self.result_callback = result_callback
        
    #----------------------------------------------------------------------
    def build_service_driver(self, target_host, target_port):
        """"""
        _id = getuuid()
        return VikitServiceDriver(id=_id,
                                  host=target_host,
                                  port=target_port,
                                  cryptor=self.cryptor,
                                  ack_timeout=self.ack_timeout,
                                  retry_timeout=self.retry_times,
                                  result_callback=self.result_callback)
        
    
    