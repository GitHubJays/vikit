#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 06/24/17
"""

########################################################################
class NotifyConfig(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        self._list_adaptor_and_its_config = []
        
    #----------------------------------------------------------------------
    def add_adaptor(self, adaptor_name, config):
        """"""
        self._list_adaptor_and_its_config.append((adaptor_name, config))
    
    @property
    def adaptors(self):
        """"""
        return [adaptor(params) for adaptor, params in \
                self._list_adaptor_and_its_config]
    
    
    
    