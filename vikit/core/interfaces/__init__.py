#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Interfaces
  Created: 06/16/17
"""

from abc import ABCMeta, abstractmethod

########################################################################
class ServerIf():
    """"""
    
    __metaclass__ = ABCMeta
    

    @abstractmethod
    def run(self, addr, async=False):
        """"""
        pass
    

########################################################################
class ClientIf():
    """"""
    
    __metaclass__ = ABCMeta

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
        
    
    
    
    