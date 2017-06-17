#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: function test
  Created: 06/17/17
"""

import time

from twisted.internet import reactor

from vikit.core.platform import vikitplatform
from vikit.core.servicenode import vikitservicenode
from vikit.core.launch.twistedlaunch import TwistdConnector, TwistdLauncher
from vikit.core.eventemitter import twistedemitter

#
# start launcher
#
platform = vikitplatform.VikitPlatform('1')
launcher = TwistdLauncher(platform)
launcher.serve(port=7077, net_if='')

#
# connecting
#
node = vikitservicenode.VikitServiceNode('2')
connector = TwistdConnector(node)
connector.connect('127.0.0.1', 7077)


#
# start
#
pemitter = twistedemitter.TwistedPlatformEventEmitter(launcher)

#
# test start service
#
#----------------------------------------------------------------------
def test_start_service():
    """"""
    global pemitter
    pemitter.start_service('2', '33', 'demo', {'port':7034,
                                               'net_if':''})    
    
reactor.callLater(2, test_start_service)

#
# test check service
#
#----------------------------------------------------------------------
def test_service():
    """"""
    pemitter.get_service_info()

reactor.callLater(2.5, test_service)


#
# shutdown function test
#
#----------------------------------------------------------------------
def stop():
    """"""
    reactor.stop()

reactor.callLater(5, stop)

reactor.run()