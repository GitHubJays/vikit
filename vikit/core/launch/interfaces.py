#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Interfaces
  Created: 06/17/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

########################################################################
class LaunchableIf(object):
    """"""

    pass
    
    

########################################################################
class LauncherIf(LaunchableIf):
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
    
    @abstractmethod
    def get_info(self):
        """"""
        pass  
    
    @abstractproperty
    def working(self):
        """"""
        pass
    

########################################################################
class ConnecterIf(LaunchableIf):
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
    
    @abstractproperty
    def working(self):
        """"""
        pass
    

    
    