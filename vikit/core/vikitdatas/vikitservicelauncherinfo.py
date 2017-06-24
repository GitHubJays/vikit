#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define VikitServiceLauncherInfo
  Created: 06/17/17
"""

from . import base

########################################################################
class VikitServiceLauncherInfo(base.VikitDatas):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, **config):
        """Constructor"""
        self.config = config
        
    #----------------------------------------------------------------------
    def get_dict(self):
        """"""
        return self.config
    
    @property
    def port(self):
        """"""
        return self.config.get('port')
        
    
    