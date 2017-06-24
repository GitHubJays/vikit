#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Adaptor Base
  Created: 06/24/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

########################################################################
class AdaptorBase(object):
    """"""

    __metaclass__ = ABCMeta
        
    @abstractmethod
    def send(self, result):
        """"""
        
    @abstractproperty
    def config(self):
        """return config {dict}"""
        
        
        
    
    