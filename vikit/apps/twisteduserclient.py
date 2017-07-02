#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: User Client
  Created: 06/24/17
"""

import time
import random

from pprint import pprint
from scouter.sop import FSM

from twisted.internet import reactor

from ..core.basic import result
from ..core import vikitlogger
from ..core.actions import result_actions
from ..core.vikitclient import vikitagent, vikitagentpool
from ..core.launch import twistedlaunch
from ..core.eventemitter import twistedemitter
from . import interfaces
from . import _config
from ..core.utils import getuuid, singleton
from ..core.vikitdatas import vikittaskfeedback, vikitserviceinfo
from ..core import resultexchanger

logger = vikitlogger.get_client_logger()

ClientConfig = _config.ClientConfig

#
# define states
#
state_START = 'start'
state_CONNECTED = 'connected'
state_WORKING = 'working'
state_ERROR = 'error'
state_END = 'end'

# start -> connected
action_STARTUP = 'action_startup'
# connected -> working
action_WORK = 'action_working'
# working -> end
action_SHUTDOWN = 'action_shutdown'
# connected -> error
action_CONNECTED_ERROR = 'action_error'
# error -> end
action_DIE = 'action_die'

_NO_DESC = ['PERSISTENCE_FUNC',
            'EXPORT_FUNC',
            'INPUT_CHECK_FUNC',
            'SEARCH_FUNC']

########################################################################
class _AgentWraper(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, agent, service_timeout=30, desc=None):
        """Constructor"""
        self._dict_service_record = {}
        self.service_timeout = service_timeout
        self.desc = desc
        
        assert isinstance(agent, vikitagent.VikitAgent)
        self.agent = agent
    
    
    #----------------------------------------------------------------------
    def update_addr(self, service_id, addr, update_time):
        """"""
        if not self._dict_service_record.has_key(service_id):
            _ = self._dict_service_record[service_id] = {}
        else:
            _ = self._dict_service_record.get(service_id)
            
        _['addr'] = addr
        _['update_time'] = update_time
    
    #----------------------------------------------------------------------
    def shrink(self):
        """"""
        def pick_timeout_service_id(id):
            _d = self._dict_service_record.get(id)
            if _d:
                return int(self.service_timeout) < \
                       int(time.time()) - int(_d['update_time'])
            else:
                return True
        ids = filter(pick_timeout_service_id, self._dict_service_record.keys())
        logger.info('[agent:{}] filtered ids:{}'.\
                    format(self.agent.module_name, ids))
        for i in ids:
            del self._dict_service_record[i]
            
        
            
    #----------------------------------------------------------------------
    def select_service(self):
        """"""
        service_id = None
        logger.info('[agent:{}] current service record: {}'.\
                    format(self.agent.module_name, self._dict_service_record))
        if len(self._dict_service_record) > 0:
            service_id = random.choice(self._dict_service_record.keys())
        else:
            logger.warn('[agent:{}] no valid service can be used.'.\
                        format(self.agent.module_name))
        
        return service_id
            
        
        
    #----------------------------------------------------------------------
    def execute(self, task_id, params, offline=False):
        """"""
        _service_id = self.select_service()
        _addr = self._dict_service_record.get(_service_id).get('addr')
        
        if not _addr:
            return False

        if offline:
            return self.agent.execute_offline(task_id, params, addr=_addr)
        else:
            return self.agent.execute(task_id, params, addr=_addr)
    

########################################################################
class TwistedClient(interfaces.AppInterfaces, singleton.Singleton):
    """"""
    
    _fsm = FSM(state_START, state_END,
               [state_CONNECTED, state_END,
                state_ERROR, state_START, 
                state_WORKING, ])
    
    _fsm.create_action(action_STARTUP, state_START, state_CONNECTED)
    _fsm.create_action(action_WORK, state_CONNECTED, state_WORKING)
    _fsm.create_action(action_SHUTDOWN, state_WORKING, state_END)
    _fsm.create_action(action_CONNECTED_ERROR, state_START, state_ERROR)
    
    
    
    task_recorder = resultexchanger.TaskIdCacher('client_tasks.pkl')
    

    #----------------------------------------------------------------------
    def __init__(self, id=None, config=None):
        """Constructor"""
        self._id = id if id else getuuid()
        self.config = config if config else _config.ClientConfig()
        assert isinstance(self.config, ClientConfig)
        
        logger.info('[client] initing id:{} and config'.format(self.id))
        
        #
        # record task and its callback chains
        #
        self._dict_callback_chains_for_every_task = {}
        
        #
        # record agents
        #
        self._dict_agent = {}        

        #
        # init agentpool
        #
        logger.info('[client] config platform client to retrieve botnet information')
        
        self.agentpool_entity = vikitagentpool.VikitClientAgentPool(self.id)
        self.__connector_agentpool = twistedlaunch.TwistdConnector(
                                                                  self.agentpool_entity)
        self.agentpool_emitter = twistedemitter.TwistdClientAgentPoolEmitter(self.__connector_agentpool,
                                                                             self.config.default_update_interval)
        self.agentpool_emitter.regist_on_service_update(self.on_service_update)
        self.agentpool_emitter.regist_on_receive_offline_result(self.on_receive_offline_result)
        
        logger.info('[client] config platform client successfully')
        
        
    
    @property
    def id(self):
        """"""
        return self._id
        
    @property
    def state(self):
        """"""
        return self._fsm.state
    
    @property
    def entity(self):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        #
        # start connector
        #
        logger.info('[client] connecting platform')
        self.__connector_agentpool.connect(self.config.platform_host,
                                           self.config.platform_port,
                                           self.config.cryptor,
                                           self.config.ack_timeout,
                                           self.config.retry_times,
                                           self.config.connect_timeout)
        
        #
        # update available service
        #
        self._start_update_services()
        
        logger.info('[client] start require offline tasks')
        #
        # update offline tasks
        #
        self._start_require_offline_tasks()
        
    
    #----------------------------------------------------------------------
    def _start_update_services(self):
        """"""

        logger.info('[client] connected platform successfully')
        logger.info('[client] start update services')
        self.agentpool_emitter.start_update_services(self.config.default_update_interval)
    
    #----------------------------------------------------------------------
    def _start_require_offline_tasks(self):
        """"""
        self.agentpool_emitter.start_require_offline_tasks(self.task_recorder, \
                                                           interval=self.config.default_update_interval)
            
    
    #----------------------------------------------------------------------
    def shutdown(self):
        """"""
        logger.info('[client] shutdown client!')
        #
        # clean the resource
        #
        self._dict_agent.clear()
        self.task_recorder.save()
        
        #
        #
        #
        if reactor.running:
            reactor.stop()
    
    #----------------------------------------------------------------------
    def mainloop_start(self):
        """"""
        logger.info('[client] run main loop')
        if not reactor.running:
            reactor.run()
        logger.info('[client] exit main loop!')
        
    #----------------------------------------------------------------------
    def mainloop_stop(self):
        """"""
        logger.info('[client] stop main loop')
        if reactor.running:
            reactor.stop()

    #
    # passive 
    #
    #----------------------------------------------------------------------
    def on_service_update(self, services):
        """"""
        #logger.debug('[client] got services from platform! {}'.format(services))
        #
        # update services  
        #
        if self.state == state_START:
            self._fsm.action(action_STARTUP)
            self._fsm.action(action_WORK)
        self.update_agentwrapper_from_services(services)
    
    #----------------------------------------------------------------------
    def build_agent(self, module_name):
        """"""
        _a = vikitagent.VikitAgent(module_name,
                                   self.config.ack_timeout,
                                   self.config.retry_times,
                                   self.config.cryptor,
                                   self.config.connect_timeout)
        _a.regist_result_callback(self.on_receive_result)
        return _a
    
    #----------------------------------------------------------------------
    def update_agentwrapper_from_services(self, service_infos):
        """"""
        for service_id, service_info in service_infos.items():
            logger.debug('[client] updateting service_id:{}'.format(service_id))
            _sinfo_obj = service_info.get('service_info')
            assert isinstance(_sinfo_obj, vikitserviceinfo.VikitServiceInfo)
            
            update_time = service_info.get('update_timestamp')
            logger.debug('[client] last update time: {}'.format(update_time))
            
            #
            # addr
            #
            _port = _sinfo_obj.linfo.port
            _ip = service_info.get('ip')
            _addr = (_ip, _port)
            logger.debug('[client] addr: {}'.format(_addr))
            
            #
            # module_name
            #
            _name = _sinfo_obj.desc.module_name
            
            #
            # build agent
            #
            if not self._dict_agent.has_key(_name):
                #
                # desc
                #
                desc = _sinfo_obj.desc.get_dict().get('mod_info')
                for i in _NO_DESC:
                    if desc.has_key(i):
                        del desc[i]
                _desc = desc
                
                _agent = self.build_agent(_name)
                _wraper = _AgentWraper(_agent, self.config.service_timeout, desc=_desc)
                self._dict_agent[_name] = _wraper
            else:
                _wraper = self._dict_agent.get(_name)
                
            assert isinstance(_wraper, _AgentWraper)
            
            logger.debug('[client] update addr pool: service_id:{} addr:{} update_time:{} module_name:{}'.\
                        format(service_id, _addr, update_time, _name))
            _wraper.update_addr(service_id, _addr, update_time)
        
        self.shrink_agentwarpper()
        logger.debug('[client] now all agents: {}'.format(self._dict_agent))
            
            
    #----------------------------------------------------------------------
    def shrink_agentwarpper(self):
        """"""
        for name, obj in self._dict_agent.items():
            obj.shrink()
    
    #----------------------------------------------------------------------
    def on_receive_result(self, result_dict, *v, **kw):
        """"""
        _task_id = result_dict.get('task_id')
        #
        # remove result record and save immediately
        #
        self.task_recorder.remove_one(_task_id)
        self.task_recorder.save()
        
        #
        # process
        #
        logger.info('[client] got a result: {}'.format(result_dict))
        
        #
        # get callback chains and call each 
        #
        _callbacks = self._dict_callback_chains_for_every_task.get(_task_id, [])
        
        _result = result_dict
        for callback in _callbacks:
            _result = callback(_result)
            
        # clean
        del self._dict_callback_chains_for_every_task[_task_id]
    
    #----------------------------------------------------------------------
    def on_receive_offline_result(self, result_submit_action):
        """"""
        assert isinstance(result_submit_action, result_actions.SubmitResultAction)
        
        _values = result_submit_action.result_dict.values()
        for i in _values:
            logger.debug('[client] got offline result: {}'.format(i))
            assert isinstance(i, result.Result)
            self.on_receive_result(i._dict_obj)
    
    #
    # active action
    #
    #----------------------------------------------------------------------
    @_fsm.onstate(state_CONNECTED, state_WORKING)
    def execute(self, module_name, params, offline=False, task_id=None, callback_chains=[], ):
        """"""
        state = False
        
        task_id = task_id if task_id else getuuid()

        #_fd = vikittaskfeedback.VikitTaskFeedback()
        
        _wrapper = self._dict_agent.get(module_name)
        if not isinstance(_wrapper, _AgentWraper):
            raise ClientError('not a valid ')
        
        #
        # record task / record callback
        #
        if not self._dict_callback_chains_for_every_task.has_key(task_id):
            self._dict_callback_chains_for_every_task[task_id] = []
        
        for callback in callback_chains:
            assert callable(callback)
            self._dict_callback_chains_for_every_task[task_id].append(callback)
        
        #
        # execute and recoud
        #
        self.task_recorder.push_one(task_id)
        if _wrapper.execute(task_id, params, offline=offline):
            pass
        else:
            self.task_recorder.remove_one(task_id)
            raise ClientError('execute faild')
    
    @_fsm.onstate(state_WORKING, state_CONNECTED)
    def get_available_modules(self):
        """"""
        return self._dict_agent.keys()
    
    @_fsm.onstate(state_WORKING, state_CONNECTED)
    def get_help_for_module(self, module_name):
        """"""
        _wraper = self._dict_agent.get(module_name)
        if _wraper:
            assert isinstance(_wraper, _AgentWraper)
            return _wraper.desc
        else:
            return None
        

########################################################################
class ClientError(Exception):
    """"""

    
    
    