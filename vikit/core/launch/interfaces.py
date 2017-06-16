#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Interfaces
  Created: 06/17/17
"""

from abc import ABCMeta, abstractmethod

########################################################################
class LauncherIf(object):
    """"""
    
    __metaclass__ = ABCMeta

    #----------------------------------------------------------------------
    def __init__(self, service):
        """Constructor"""
        self.service = service
        
    
    @abstractmethod
    def serve(self, **config):
        """"""
        pass
    
    @abstractmethod
    def stop(self):
        """"""
        pass
    

########################################################################
class ConnecterIf(object):
    """"""
    
    __metaclass__ = ABCMeta

    #----------------------------------------------------------------------
    def __init__(self, client):
        """Constructor"""
        self.client = client
        
    @abstractmethod
    def connect(self, **config):
        """"""
        pass
    
    @abstractmethod
    def stop(self):
        """"""
        pass
        
    
    