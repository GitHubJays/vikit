#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: ServiceNode Test
  Created: 06/19/17
"""

from twisted.internet import reactor

from vikit.core.servicenode import vikitservicenode
from vikit.core.eventemitter import twistedemitter
from vikit.core.launch.twistedlaunch import TwistdConnector

n = vikitservicenode.VikitServiceNode('test', heartbeat_interval=2)
c = TwistdConnector(n)
t = twistedemitter.TwistedServiceNodeEventEmitter(c)
t.regist_start_heartbeat_callback()
c.connect('127.0.0.1', 7000)

reactor.run()