#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Welcome Packet
  Created: 06/02/17
"""

from .ackpool import Ackable, Ack

########################################################################
class WelcomeBase(Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """"""
        self._id = id
        
    @property
    def id(self):
        """"""
        return self._id

########################################################################
class WelcomeBaseACK(Ack):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """"""
        self._id = id
        
    @property
    def id(self):
        """"""
        return self._id
        


########################################################################
class PlatformWelcome(WelcomeBase):
    """"""


########################################################################
class PlatformWelcomeACK(WelcomeBaseACK):
    """"""

########################################################################
class ServiceAdminWelcome(WelcomeBase):
    """"""
    
########################################################################
class ServiceAdminWelcomeAck(WelcomeBaseACK):
    """"""

        
    
    
        
        
    
    


        
    
    