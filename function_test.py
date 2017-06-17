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

time.sleep(5)

platform
print(platform)
print(platform._dict_service_node_recorder)

#
# start
#
#pemitter = twistedemitter.TwistedPlatformEventEmitter(launcher)
#pemitter.start_service('1', '33', 'demo', {'port':7034,
                                           #'net_if':''})

reactor.run()