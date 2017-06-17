#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define VikitDatas
  Created: 06/17/17
"""

from abc import ABCMeta, abstractmethod

########################################################################
class VikitDatas(object):
    """"""

    @abstractmethod
    def get_dict(self):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def __getattr__(self, key):
        """"""
        if hasattr(self, 'config'):
            return self.config.get(key)
        else:
            return None
        
    