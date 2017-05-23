#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Control run items
  Created: 05/22/17
"""

from twisted.internet import reactor

from . import platform



#----------------------------------------------------------------------
def run_platform(name, interface, port, cryptor=None):
    """"""
    platform_obj = platform.Platform(name, interface, port)
    
    reactor.listenTCP(port, 
                      platform.PlatformTwistedConnFactory(platform_obj,
                                                          cryptor))
    reactor.run()
