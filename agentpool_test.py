#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Agent Pool Test
  Created: 06/21/17
"""

import time

from twisted.internet import reactor

from vikit.core.vikitclient import vikitagentpool
from vikit.core.launch import twistedlaunch
from vikit.core.eventemitter import twistedemitter

pool = vikitagentpool.VikitClientAgentPool()
connector = twistedlaunch.TwistdConnector(pool)
connector.connect('127.0.0.1', 7000)

emitter = twistedemitter.TwistdClientAgentPoolEmitter(connector)

#----------------------------------------------------------------------
def _start_update():
    """"""
    
    emitter.start_update_services()
    
reactor.callLater(2, _start_update)
    
#----------------------------------------------------------------------
def _start_get_services():
    """"""
    
    print emitter.get_service()   

reactor.callLater(4, _start_get_services)
reactor.run()