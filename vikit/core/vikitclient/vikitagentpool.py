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
    # record servcies
    #
    _dict_service_infos = {}
    
    #
    # id
    #
    platform_id = None

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
        
        _fdsd = self.get_sender(self.platform_id)
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
            