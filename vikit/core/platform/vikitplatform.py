#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: VikitPlatform
  Created: 06/17/17
"""

from ..basic import vikitbase
from ..utils.singleton import Singleton
from ..actions import welcome_action


########################################################################
class VikitPlatform(vikitbase.VikitBase, Singleton):
    """"""
    
    _dict_service_node_recorder = {}
    _id = ''
    _service_infos = []

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        self._id = id
    
    @property
    def id(self):
        """"""
        return self._id
    
    #----------------------------------------------------------------------
    def on_received_obj(self, obj, *args, **kw):
        """"""
        if isinstance(obj, welcome_action.VikitWelcomeAction):
            self.regist_service_node(obj.id, **kw)
        else:
            raise NotImplemented()
    
    #----------------------------------------------------------------------
    def on_connection_lost(self, *v, **kw):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def on_connection_made(self, *v, **kw):
        """"""
        pass
    
    #
    # utils
    #
    #----------------------------------------------------------------------
    def regist_service_node(self, service_node_id, **record):
        """"""
        if not self._dict_service_node_recorder.has_key(service_node_id):
            self._dict_service_node_recorder[service_node_id] = {}
        
        self._dict_service_node_recorder[service_node_id].update(record)
        
    
    #----------------------------------------------------------------------
    def has_service_node(self, service_node_id):
        """"""
        return self._dict_service_node_recorder.has_key(service_node_id)
    
    #----------------------------------------------------------------------
    def get_service_node_record(self, service_node_id):
        """"""
        return self._dict_service_node_recorder.get(service_node_id, {})
    
    #----------------------------------------------------------------------
    def get_service_info(self):
        """"""
        return self._service_infos
        
    
    

