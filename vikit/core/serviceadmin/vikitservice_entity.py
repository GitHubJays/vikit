#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Vikit Service
  Created: 06/05/17
"""

import types
import os

from scouter.sop import FSM
from twisted.internet.task import LoopingCall

from ..basic import mod, result
from ..common import baseprotocol, serviceop
from ..utils import getuuid

#
# client relavent
#
########################################################################
class _VikitTask(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, params):
        """Constructor"""
        self._id = id
        assert isinstance(params, dict)
        self._params = params
        self._result = None
        
        self._finished_flag = False
    
    @property
    def id(self):
        """"""
        return self._id
    
    @property
    def params(self):
        """"""
        return self._params
    
    @property
    def result(self):
        """"""
        return self._result
    
    @result.setter
    def result(self, v):
        """"""
        assert isinstance(v, dict)
        self._finished_flag = True
        return result.Result(v)
    
    @property
    def finished(self):
        """"""
        return self._finished_flag
        

########################################################################
class _VikitClient(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, conn, ack_timeout=10, retry_times=5):
        """Constructor"""
        #
        # config basic attrs
        #
        self._id = id
        self.conn = conn
        assert isinstance(self.conn, baseprotocol.VikitProtocol)
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        
        self._task_map = {}
        
    @property
    def id(self):
        """"""
        return self._id
    
    #----------------------------------------------------------------------
    def add_task(self, task_id, params):
        """"""
        if self._task_map.has_key(task_id):
            raise StandardError('[!] repeat task id')
        else:
            self._task_map[task_id] = _VikitTask(task_id, params)
    
    #----------------------------------------------------------------------
    def finish_task(self, task_id, result):
        """"""
        assert self._task_map.has_key(task_id)
        _t = self._task_map.get(task_id)
        assert isinstance(_t, _VikitTask)
        _t.result = result
        
        self.conn.send(obj, self.ack_timeout, self.retry_times)
    
    #----------------------------------------------------------------------
    def task_ids(self):
        """"""
        return self._task_map.keys()
        
        
########################################################################
class _VikitClientPool(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, ack_timeout=10, retry_times=5):
        """Constructor"""
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        
        self._client_map = {}
    
    #----------------------------------------------------------------------
    def regist_client(self, id, conn):
        """"""
        _retclient = _VikitClient(id, conn, self.ack_timeout, self.regist_client)
        
        assert not self._client_map.has_key(id)
        self._client_map[id] = _retclient
    
    #----------------------------------------------------------------------
    def unregist_client(self, client_id):
        """"""
        if self._client_map.has_key(client_id):
            del self._client_map[client_id]
        
    
    #----------------------------------------------------------------------
    def regist_task(self, client_id, task_id, params):
        """"""
        _c = self.get_client_by_id(client_id)
        assert isinstance(_c, _VikitClient)
        
        _c.add_task(task_id, params)
    
    #----------------------------------------------------------------------
    def finish_task(self, client_id, task_id, result):
        """"""
        _c = self.get_client_by_id(client_id)
        assert isinstance(_c, _VikitClient)
        
        _c.finish_task(task_id, result)
        
    
    #----------------------------------------------------------------------
    def get_client_by_id(self, id):
        """"""
        return self._client_map.get(id)

    #----------------------------------------------------------------------
    def has_client(self, client_id):
        """"""
        return self._client_map.has_key(client_id)
        
        
    

#
# define state
#
state_START = 'start'

# action: start_error INITING->ERROR
# action: runtime_error WORKING->ERROR
state_ERROR = 'error'

# action: start START->INITING
state_INITING = 'initing'

# action: start_finish INITING->WORKING
state_WORKING = 'working'

# action finish WORKING->END
# action error_to_die ERROR->END
state_END = 'end'

_all_states = [state_END, 
               state_ERROR,
               state_INITING,
               state_START,
               state_WORKING]

_CURRENT_PATH_ = os.path.dirname(__file__)
_CURRENT_MODS_PATH_ = os.path.join(_CURRENT_PATH_, '../../mods/')

########################################################################
class VikitServiceConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, min_threads=5, max_threads=20, debug=True,
                 loop_interval=0.2, adjust_interval=3, diviation_ms=100,
                 default_mod_paths=[_CURRENT_MODS_PATH_,],
                 cryptor=None, result_update_interval=1, ack_timeout=10,
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
    


########################################################################
class VikitService(object):
    """"""
    
    fsm = FSM(state_START, state_END,
              _all_states)

    #----------------------------------------------------------------------
    def __init__(self, id, bind_port, bind_if='', config=None):
        """Constructor"""
        self._id = id
        self._bind_port = bind_port
        self._bind_if = bind_if
        
        #
        # config
        #
        self.config = config if config else VikitServiceConfig()
        assert isinstance(self.config, VikitServiceConfig)
        
        #
        # config FSM
        #
        self.action_start()
        
        #
        # config mod factory
        #
        self._mod_factory = mod.ModFactory(self.config.min_threads,
                                           self.config.max_threads,
                                           self.config.debug,
                                           self.config.loop_interval,
                                           self.config.adjust_interval,
                                           self.config.diviation_ms)
        
        #
        # client pool
        #
        self._client_pool = _VikitClientPool(self.config.ack_timeout,
                                             self.config.ack_retry_times)
        
        #
        # record task_id map client_id
        #
        self._dict_task_id_map_client_id = {}
        
        #
        # set collecting result loopingcall
        #
        self._loopingcall_collecting_result = LoopingCall(self._collect_result)
        
    #
    # basic property
    #
    @property
    def id(self):
        """"""
        return self._id
    
    
    #
    # define actions for fsm
    #
    @fsm.transfer(state_START, state_INITING)
    def action_start(self):
        """"""
        pass
    
    @fsm.transfer(state_INITING, state_WORKING)
    def action_start_finish(self):
        """"""
        self._start_collecting_result()
    
    @fsm.transfer(state_WORKING, state_END)
    def action_finish(self):
        """"""
        self.stop_collecting_result()
    
    @fsm.transfer(state_ERROR, state_END)
    def action_error_to_die(self):
        """"""
        self.stop_collecting_result()
    
    @fsm.transfer(state_INITING, state_ERROR)
    def action_start_error(self):
        """"""
        pass
    
    @fsm.transfer(state_WORKING, state_ERROR)
    def action_runtime_error(self):
        """"""
        #self.stop_collecting_result()
        self.action_error_to_die()

    #
    # core function
    #
    @fsm.onstate(state_INITING)
    def load_mod(self, module_name):
        """"""
        #
        # load mod from module name
        #
        obj = __import__(module_name)
        
        assert isinstance(obj, types.ModuleType)
        self._mod = self._mod_factory.build_standard_mod_from_module(obj)
        
        self.action_start_finish()
    
    @fsm.onstate(state_WORKING)
    def execute_task(self, client_id, task_id, params):
        """"""
        assert isinstance(self._mod, mod.ModStandard)
        assert self._client_pool.has_client(client_id)
        
        #
        # record client
        #
        self._dict_task_id_map_client_id[task_id] = client_id
        
        #
        # execute by mod
        #
        self._mod.execute(params, task_id)
    
    #----------------------------------------------------------------------
    def finish_task(self, _result):
        """"""
        assert isinstance(_result, result.Result)
        raw = _result._dict_obj
        assert raw.has_key('task_id')
        task_id = raw.get('task_id')
        client_id = self.get_client_id_by_task(task_id)
        self._client_pool.finish_task(client_id, task_id, raw)
        
        
    #----------------------------------------------------------------------
    def _collect_result(self):
        """"""
        _queue = self._mod.result_queue
        while _queue.qsize() > 0:
            _r = _queue.get()
            self.finish_task(_r)
        
        return
    
    #----------------------------------------------------------------------
    def _start_collecting_result(self):
        """"""
        #
        # reset and run
        #
        if self._loopingcall_collecting_result.running:
            self._loopingcall_collecting_result.stop()
            
        self._loopingcall_collecting_result.start(self.config.result_update_interval)
    
    #----------------------------------------------------------------------
    def stop_collecting_result(self):
        """"""
        #
        # safe stop
        #
        if self._loopingcall_collecting_result.running:
            self._loopingcall_collecting_result
    
    @fsm.onstate(state_WORKING)    
    def regist_client(self, client_id, conn):
        """"""
        self._client_pool.regist_client(client_id, conn)
    
    #----------------------------------------------------------------------
    def unregist_client(self, client_id):
        """"""
        #
        # remove from client pool
        #
        self._client_pool.unregist_client(client_id)
        
        #
        # remove tasks in client
        #
        def filter_idle_task(task):
            return task[1] == client_id
        _buffer = filter(filter_idle_task, self._dict_task_id_map_client_id.items())
        _buffer = map(lambda x: x[0], _buffer)
        
        for i in _buffer:
            del self._dict_task_id_map_client_id[i]
    
    #
    # handler
    #
    #----------------------------------------------------------------------
    def handle_welcome(self, id, conn):
        """"""
        self.service.regist_client(obj.id, self)
    
    #----------------------------------------------------------------------
    def handle_task(self, obj):
        """"""
        if isinstance(obj, serviceop.VikitTaskInProto):
            self.execute_task(client_id=obj.client_id, task_id=obj.id, params=obj.params)
        


########################################################################
class VikitServiceFactory(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_config=None):
        """Constructor"""
        #assert isinstance(service_config, VikitServiceConfig)
        #
        # set config
        #
        self.config = service_config if service_config else VikitServiceConfig()
        assert isinstance(self.config, VikitServiceConfig)
    
    #----------------------------------------------------------------------
    def build_service(self, bind_port, bind_if=''):
        """"""
        _id = getuuid()
        return VikitService(_id, bind_port, bind_if, self.config)
    
    #----------------------------------------------------------------------
    def build_service_with_config(self, bind_port, bind_if='', config=None, id=None):
        """"""
        if config == None:
            config = self.config
        
        _id = id if id else getuuid()
        return VikitService(_id, bind_port, bind_if, config)
        
        
    
    
    
        
        
    
    