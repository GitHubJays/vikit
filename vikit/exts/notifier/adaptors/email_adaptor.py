#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 06/24/17
"""

from . import adatporbase

########################################################################
class EmailAdaptor(adatporbase.AdaptorBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, **config):
        """Constructor"""
        self._config = config
        
    @property
    def config(self):
        """"""
        return self._config
        
        
    
    