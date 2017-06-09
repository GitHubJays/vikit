#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: VikitClient
  Created: 06/06/17
"""

import random

from scouter.sop import FSM
from ..basic import result
from ..common import userclientop
from . import client_forservice
from . import client_forplatform

#
# define state
#
state_START = 'start'
# action: start START->INITING
state_INITING = 'initing'
# action: start_finish INITING->WORKING
state_WORKING = 'working'
# action: start_error INITING->ERROR
# action: runtime_error WORKING->ERROR
state_ERROR = 'error'
# action: finish WORKING->END
# action: error_to_die ERROR->END
state_END = 'end'

#########################################################################
#class _Service(object):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self, id, module_name, host, port):
        #"""Constructor"""
        #self._id = id
        #self.module_name = module_name
        
        ##
        ## addr
        ##
        #self.host = host
        #self.port = port
        
    #@property
    #def id(self):
        #""""""
        #return self._id
    

#########################################################################
#class _ServiceInfo(object):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self):
        #"""Constructor"""
        #self._value_dict = {} 
    
    ##----------------------------------------------------------------------
    #def update_service(self, _service_info):
        #""""""
        #assert isinstance(_service_info, _Service)
        ##self._value_dict[_service_info] = _Service
        #assert self._value_dict.has_key(_service_info.module_name)
        #assert isinstance(self._value_dict[_service_info.module_name], dict)
            
        #self._value_dict[_service_info.module_name][_service_info.id] = _service_info
    
    ##----------------------------------------------------------------------
    #def regist_module(self, module_name):
        #""""""
        #if not self._value_dict.has_key(module_name):
            #self._value_dict[module_name] = {}
    
    ##----------------------------------------------------------------------
    #def get_services_by_module_name(self, module_name):
        #""""""
        #return self._value_dict.get(module_name)
    
    ##----------------------------------------------------------------------
    #def update(self, obj):
        #""""""
        #assert isinstance(obj, userclientop.ServiceInfo)
        
        #_infodict = obj.service_information
    

##
## _Task
##
#########################################################################
#class _Task(object):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self, id, module_name, params):
        #"""Constructor"""
        #self._id = id
        #self._module_name = module_name
        #assert isinstance(params, dict)
        #self._params = params
        
        ##
        ## priv fields
        ##
        #self._result = None
    
    #@property
    #def id(self):
        #""""""
        #return self._id
    
    #@property
    #def params(self):
        #""""""
        #return self._params
    
    #@property
    #def module_name(self):
        #""""""
        #return self._module_name
    
    ##----------------------------------------------------------------------
    #def execute(self, service_ins):
        #""""""
        #assert isinstance(service_ins, _ServiceConn)
        #_ServiceConn.execute(self.id, self.params)
    
    ##----------------------------------------------------------------------
    #def finish(self, result_dict):
        #""""""
        #self._result = result.Result(result_dict)
        
    #@property
    #def result(self):
        #""""""
        #return self._result
        
        
    
    

##
## _Service
##
#########################################################################
#class _ServiceConn(object):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self, id, module_name, conn, ack_timeout=10, retry_times=5):
        #"""Constructor"""
        #self._id = id
        #assert isinstance(conn, client_forservice.ServiceClientForUser)
        #self._conn = conn
        #self._module_name = module_name
    
        #self._ack_timeout = ack_timeout
        #self._retry_times = retry_times
        
        ##
        ## priv attrs
        ##
        #self._tasks = {}
    
    #@property
    #def id(self):
        #""""""
        #return self._id
    
    #@property
    #def conn(self):
        #""""""
        #return self._conn
    
    ##----------------------------------------------------------------------
    #def execute(self, task_id, params):
        #""""""
        #_t = userclientop.VikitTaskInProto(task_id, params, self.id)
        
        ##
        ## regist task
        ##
        #self.regist_task(task_id, params)
        
        ##
        ## execute
        ##
        #self._conn.send(obj, ack_timeout=self._ack_timeout,
                        #retry_times=self._retry_times)
        
    ##----------------------------------------------------------------------
    #def regist_task(self, task_id, params):
        #""""""
        ##
        ## new key
        ##
        #_t = _Task(task_id, self._module_name, params)
        #self._tasks[task_id] = _t

    ##----------------------------------------------------------------------
    #def get_task_by_id(self, task_id):
        #""""""
        #return self._tasks.get(task_id)
        
    
    ##----------------------------------------------------------------------
    #def finish(self, task_id, result_dict):
        #""""""
        ##
        ## got _Task
        ##
        #_t = self.get_task_by_id(task_id)
        #assert isinstance(_t, _Task)
        
        ##
        ## update _Task instance
        ##
        #_t.finish(result_dict)
    
        ##
        ## notify
        ##
        ### TODO
        ### TODO
        ### TODO

##
## _ModAgent: wrapper for the same mod services
##
#########################################################################
#class _ModAgent(object):
    #""""""

    ##----------------------------------------------------------------------
    #def __init__(self, module_name, ack_timeout=10, retry_times=5):
        #"""Constructor"""
        #self._services = {}
        
        ##
        ## basic attrs
        ##
        #self._ack_timeout = ack_timeout
        #self._retry_times = retry_times
    
    ##----------------------------------------------------------------------
    #def add_service(self, id, conn):
        #""""""
        #_sins = _ServiceConn(id, self._module_name, conn, ack_timeout=self._ack_timeout, 
                            #retry_times=self._retry_times)
        ##self._services.append(_sins)
        #self._services[id] = _sins
        
    ##----------------------------------------------------------------------
    #def select(self, by=None):
        #""""""
        #return random.choice(self._services.values())
        
    ##----------------------------------------------------------------------
    #def execute(self, task_id, params):
        #""""""
        #_s = self.select()
        #_s.execute(task_id, params)
        
    ##----------------------------------------------------------------------
    #def finish(self, client_id, task_id, result_dict):
        #""""""
        #_s = self.get_service_conn(client_id)
        #assert isinstance(_s, _ServiceConn)
        
        #_s.finish(task_id, result_dict)
    
    ##----------------------------------------------------------------------
    #def get_service_conn(self, task_id):
        #""""""
        #return self._services.get(task_id)
        
    
    

########################################################################
class VikitClientConfig():
    """"""

    #----------------------------------------------------------------------
    def __init__(self, cryptor=None, ack_timeout=10,
                 retry_times=5):
        """Constructor"""
        
        self.cryptor = cryptor
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
    
    

#
# ops:
# 1. connect/disconnect platform
# 2. add/remove service
# 3. execute/finish task
#

########################################################################
class VikitClient(object):
    """"""
    
    fsm = FSM(state_START, state_END,
              [state_END, state_ERROR,
               state_INITING, state_START,
               state_WORKING])

    #----------------------------------------------------------------------
    def __init__(self, id, service_host, service_port, config=None):
        """Constructor"""
        #
        # basic attrs
        #
        self._id = id
        self._service_host = service_host
        self._service_port = service_port
        
        #
        # config attrs
        #
        self.config = config if config else VikitClientConfig()
        assert isinstance(self.config, VikitClientConfig)
        
        #
        # bind platform
        #
        self.platform_conn = None
        
        #
        # service info
        #
        self._service_info = _ServiceInfo()
        
        
        self.action_start()
    
    @property
    def id(self):
        """"""
        return self._id
        
    @fsm.transfer(state_START, state_INITING)
    def action_start(self):
        """"""
        pass
    
    @fsm.transfer(state_INITING, state_WORKING)
    def action_start_finish(self):
        """"""
        pass
    
    @fsm.transfer(state_INITING, state_ERROR)
    def action_start_error(self):
        """"""
        pass
    
    @fsm.transfer(state_WORKING, state_ERROR)
    def action_runtime_error(self):
        """"""
        pass
    
    @fsm.transfer(state_WORKING, state_END)
    def action_finish(self):
        """"""
        pass
    
    @fsm.transfer(state_ERROR, state_END)
    def action_error_to_die(self):
        """"""
        pass
    
    
    #
    # interact with platform
    #
    #----------------------------------------------------------------------
    @fsm.onstate(state_INITING)
    def _connect_platform(self):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def _disconnect_platform(self):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def _update_service_info(self):
        """"""
        assert isinstance(self.platform_conn, client_forplatform.PlatformClientForUser)
        
        self._query_service_info()
        
        
    #----------------------------------------------------------------------
    def _query_service_info(self):
        """"""
        _query = userclientop.RequireInfo(self.id)
        self.platform_conn.send(_query, self.config.ack_timeout, self.config.retry_times)
        
    
    #----------------------------------------------------------------------
    def update_service_info(self, obj):
        """"""
        self._service_info.update(obj)
    
    #
    # serve
    # 1. connect platform
    # 2. load _ModAgent
    # 3. execute or not
    # 
    #----------------------------------------------------------------------
    def serve(self):
        """"""
        #
        # connect platform
        #
        self._connect_platform()
        
        #
        # load _ModAgent
        # 
        self._update_service_info()
    
    #
    # handle packet callback
    #
    #----------------------------------------------------------------------
    def handle_welcome(self, obj):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def handle_service_info(self, obj):
        """"""
        self.update_service_info(obj)
    
    #----------------------------------------------------------------------
    def handle_userclient_result(self, obj):
        """"""
        raise NotImplemented()
        
        
        
        
    