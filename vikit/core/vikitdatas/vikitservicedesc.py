#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define VikitServiceDesc
  Created: 06/17/17
"""

from .base import VikitDatas

########################################################################
class VikitServiceDesc(VikitDatas):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, mod_info):
        """Constructor"""
        self.id = id
        assert isinstance(mod_info, dict)
        self.mod_info = mod_info
    
    #----------------------------------------------------------------------
    def get_dict(self):
        """"""
        return {'id':self.id,
                'mod_info':self.mod_info}
        
        
        
    
    