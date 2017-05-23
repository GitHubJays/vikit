#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform Tac
  Created: 05/23/17
"""

#
# import twisted base 
#
from twisted.application import internet, service


import sys
import os

s = os.path.dirname(os.path.abspath(__file__))
sys.path.append(s)

#
# import factory
#
from twisted_factories import Platform, PlatformTwistedConnFactory

#
# set default attrs
#
port = 7001
platform_obj = Platform(name='platform', host='asdf', port='8123')

_fac = PlatformTwistedConnFactory(platform_obj)


#
# app
#
application = service.Application(platform_obj.name)
service = internet.TCPServer(port, _fac)
service.setServiceParent(application)