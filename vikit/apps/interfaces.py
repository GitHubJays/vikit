#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Basic Interfaces
  Created: 06/23/17
"""

from abc import ABCMeta, abstractmethod, abstractproperty

########################################################################
class AppInterfaces(object):
    """"""
    
    __metaclass__ = ABCMeta

    # 
    # start / stop Application
    #
    @abstractmethod
    def start(self):
        """Start Service or Start connect to Server"""
        
    @abstractmethod
    def shutdown(self):
        """Shutdown the App"""
        
    #
    # basic property
    #
    @abstractproperty
    def state(self):
        """Current State for the current app"""
        
    @abstractproperty
    def entity(self):
        """"""
        
    
    #
    # operation mainloop
    #
    @abstractmethod
    def mainloop_start(self):
        """"""
    
    @abstractmethod
    def mainloop_stop(self):
        """"""
        
        
        
        
    
        
        
    
    