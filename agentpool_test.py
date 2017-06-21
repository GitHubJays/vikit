#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Agent Pool Test
  Created: 06/21/17
"""

from twisted.internet import reactor

from vikit.core.vikitclient import vikitagentpool
from vikit.core.launch import twistedlaunch
from vikit.core.eventemitter import twistedemitter

pool = vikitagentpool.VikitClientAgentPool()
connector = twistedlaunch.TwistdConnector(pool)
connector.connect('127.0.0.1', 7000)

emitter = twistedemitter.TwistdClientAgentPoolEmitter(connector)
emitter.get_service()