#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: VikitPlatform
  Created: 06/17/17
"""

import time

from ..basic import vikitbase
from ..utils.singleton import Singleton
from ..actions import welcome_action, heartbeat_action
from ..vikitdatas import vikitserviceinfo

########################################################################
class VikitPlatform(vikitbase.VikitBase, Singleton):
    """"""
    
    _dict_service_node_recorder = {}
    _id = ''
    _dict_service_infos = {}

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
        elif isinstance(obj, heartbeat_action.HeartBeatAction):
            self.update_from_heartbeat(obj)
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
    
    #----------------------------------------------------------------------
    def update_from_heartbeat(self, heartbeat_obj):
        """"""
        #
        # update service node health info
        #
        hinfobj = heartbeat_obj.health_info
        self.update_health_info(heartbeat_obj.service_node_id, hinfobj)
        
        #
        # update services info
        #
        services = heartbeat_obj.service_infos
        self.update_service_info(services)
    
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
    def update_health_info(self, service_node_id, health_info_obj):
        """"""
        #
        # got record
        # 
        _record = self.get_service_node_record(service_node_id)
        
        #
        # add health information
        #
        _record['health_info'] = health_info_obj.get_dict()
    
    #----------------------------------------------------------------------
    def update_service_info(self, service_infos):
        """"""
        def _update_services(service_info_obj):
            assert isinstance(service_info_obj, vikitserviceinfo.VikitServiceInfo)
            if not self._dict_service_infos.has_key(service_info_obj.id):
                self._dict_service_infos[service_info_obj.id] = {}
            
            #
            # update timestamp
            #
            self._dict_service_infos[service_info_obj.id]['update_timestamp'] = time.time()
            
            #
            # update service info data
            #
            self._dict_service_infos[service_info_obj.id]['service_info'] = service_info_obj
        
        map(_update_services, service_infos)
        
    
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
        return self._dict_service_infos
    
    
    #----------------------------------------------------------------------
    def remove_service_by_id(self, service_id):
        """"""
        if self._dict_service_infos.has_key(service_id):
            del self._dict_service_infos[service_id]
        else:
            pass
    
    

