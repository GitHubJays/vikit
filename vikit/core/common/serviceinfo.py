#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service Info
  Created: 06/09/17
"""

########################################################################
class ServiceInfo(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, module_name, host, port):
        """Constructor"""
        self.id = id
        self.module_name = module_name
        self.host = host
        self.port = port
    

########################################################################
class SerivceSetInfo(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._service_set = {}
        
    #----------------------------------------------------------------------
    def update_service(self, service_info):
        """"""
        isinstance(service_info, ServiceInfo)
        
        mn = service_info.module_name
        
        #
        # initial
        #
        if not self._service_set.has_key(mn):
            self._service_set[mn] = {}
        
        self._service_set[mn]['id'] = service_info.id
        self._service_set[mn]['addr'] = {}
        self._service_set[mn]['addr']['host'] = service_info.host
        self._service_set[mn]['addr']['port'] = service_info.port
    
    @property
    def value(self):
        """"""
        return self._service_set
        
        
    
    