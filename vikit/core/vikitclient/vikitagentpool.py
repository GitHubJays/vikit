#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client Agent Pool
  Created: 06/21/17
"""

from ..actions import welcome_action, servicenode_actions, platform_actions
from ..basic import vikitbase
from ..utils import singleton
from ..vikitdatas import vikitserviceinfo, vikitservicedesc, vikitservicelauncherinfo
#from . import vikitagent

#
# states defines
#
state_WORKING = 'working'
state_PENDING = 'pending'

########################################################################
class VikitClientAgentPool(vikitbase.VikitBase, singleton.Singleton):
    """"""
    
    # 
    # if disable_default_connectionMade is True, the default \ 
    #    connectionMade (send WelcomeAction) is disable
    #
    disable_default_connectionMade = True
    
    #
    # record servcies/agents
    #
    _dict_service_infos = {}
    _dict_agents = {}
    
    #
    # id
    #
    platform_id = None
    
    #
    # callback chains
    #
    _callback_chains_service_update = []
    

    #----------------------------------------------------------------------
    def __init__(self, id='vikitclientagentpool'):
        """Constructor"""
        self._id = id
        
        self._state = state_PENDING
    
        
    @property
    def id(self):
        """"""
        return self._id
        
    #
    # operation
    #
    #----------------------------------------------------------------------
    def get_service(self):
        """"""
        return self._dict_service_infos
    
    #----------------------------------------------------------------------
    def update_services_list(self):
        """"""
        _sender = self.get_sender(self.platform_id)
        
        #
        # build request service infos
        #
        _rsinfos = platform_actions.VikitRequestServiceListPlatform(self.id)
        
        _sender.send(_rsinfos)
    
    #----------------------------------------------------------------------
    def regist_on_service_update(self, callback):
        """"""
        assert callable(callback)
        self._callback_chains_service_update.append(callback)
    
    #
    # system callback
    # 
    #----------------------------------------------------------------------
    def on_connection_lost(self, *v, **kw):
        """"""
        self._dict_service_infos.clear()
    
    #----------------------------------------------------------------------
    def on_connection_made(self, *v, **kw):
        """"""
        _sender = kw.get('sender')
        assert _sender is not None
        
        _fdsd = _sender 
        _fdsd.send(welcome_action.VikitClientWelcomeAction(self.id))
    
    #----------------------------------------------------------------------
    def on_received_obj(self, obj, *v, **kw):
        """"""
        if self._state == state_PENDING:
            if isinstance(obj, welcome_action.VikitWelcomeAction):
                self.handle_welcome_action(obj)
            else:
                pass
        else:
            if isinstance(obj, platform_actions.VikitResponseServiceListPlatform):
                self.handle_response_servicelist_action(obj)
            pass
    
    #----------------------------------------------------------------------
    def on_service_update(self, services):
        """"""
        for i in self._callback_chains_service_update:
            i(services)
        
    #----------------------------------------------------------------------
    def handle_welcome_action(self, obj, *v, **kw):
        """"""
        #
        # handle obj
        #
        self.platform_id = obj.id
        
        #
        # set state
        #
        self._state = state_WORKING
    
    #----------------------------------------------------------------------
    def handle_response_servicelist_action(self, obj, *v, **kw):
        """"""
        assert isinstance(obj, platform_actions.VikitResponseServiceListPlatform)
        
        _dict_services = obj.services_dict
        
        #
        # update services
        #
        self._dict_service_infos.clear()
        self._dict_service_infos.update(_dict_services)
    
        self.on_service_update(self._dict_service_infos)
        ##
        ## update agent from services
        ##
        #for i in self._dict_service_infos.iteritems():
            
            ##
            ## retrieve info
            ##
            #_sid, _infos = i
            #_snid = _infos.get('service_node_id')
            #_update_time = _infos.get('update_timestamp')
            #_info_obj = _infos.get('service_info')
            
            #assert isinstance(_info_obj, vikitserviceinfo.VikitServiceInfo)
            #_info_desc = _info_obj.desc
            #assert isinstance(_info_desc, vikitservicedesc.VikitServiceDesc)
            
            ##
            ## update agent
            ##
            #module_name = _info_desc.mod_info.get('module_name')
            #if not self._dict_agents.has_key(module_name):
                #_agent = vikitagent.VikitAgent(module_name, self._ack_timeout,
                                               #self._retry_times, self._cryptor,
                                               #self._connect_timeout)
                
                #self._dict_agents[module_name] = {'agent':_agent}
            
            #_agent_infos = self._dict_agents.get(module_name)
            #_agent_infos['update_timestamp'] = _update_time
            #_agent = _agent_infos.get('agent')
            
            #raise NotImplementedError()
            
            