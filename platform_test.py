#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4>
  Purpose: 
  Created: 06/19/17
"""

import time
from twisted.internet import reactor

from vikit.core.platform import vikitplatform
from vikit.core.launch import twistedbase
from vikit.core.launch.twistedlaunch import TwistdLauncher
from vikit.core.eventemitter import twistedemitter

p = vikitplatform.VikitPlatform('platform')
l = TwistdLauncher(p)
l.serve(port=7000, net_if='')
emitter = twistedemitter.TwistedPlatformEventEmitter(l)


#----------------------------------------------------------------------
def _start_service():
    """"""

    emitter.start_service('test', '123', 'demo', {'port':7034,
                                                  'net_if':''})
    
#----------------------------------------------------------------------
def _stop_service():
    """"""
    print emitter.get_service_info()
    emitter.stop_service(service_id='123')
    
    
reactor.callLater(5, _start_service)
#reactor.callLater(7, _stop_service)

#----------------------------------------------------------------------
def _stop_platform():
    """"""
    print('[platform] shuting down')
    emitter.shutdown()
#reactor.callLater(13, _stop_platform)

reactor.run()
