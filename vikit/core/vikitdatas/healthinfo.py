#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Build Health Info
  Created: 06/18/17
"""

from . import base

########################################################################
class HealthInfo(base.VikitDatas):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, cpu_percent=None, ram_percent=None):
        """Constructor"""
        self.cpu_percent = cpu_percent
        self.ram_percent = ram_percent
        self._dict_obj = {}
        self._dict_obj['cpu_percent'] = self.cpu_percent
        self._dict_obj['ram_percent'] = self.ram_percent
    
    #----------------------------------------------------------------------
    def get_dict(self):
        """"""
        return self._dict_obj
        
    
    