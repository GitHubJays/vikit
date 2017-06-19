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
print('[+] STARTING Platform')
platform = vikitplatform.VikitPlatform('1')
launcher = TwistdLauncher(platform)
launcher.serve(port=7077, net_if='')
print('[+] START Platform SUCCESS')

#
# connecting
#
print('[+] START SERVICE NODE')
node = vikitservicenode.VikitServiceNode('2')
connector = TwistdConnector(node)
connector.connect('127.0.0.1', 7077)
nodemitter = twistedemitter.TwistedServiceNodeEventEmitter(connector)
nodemitter.regist_start_heartbeat_callback()
print('[+] START ServiceNode Success')


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
    print('[*] Start service demo')

print('[2] 2 later call start service')    
reactor.callLater(2, test_start_service)

#
# test check service
#
#----------------------------------------------------------------------
def test_service():
    """"""
    print('[*] start get service')
    s = pemitter.get_service_info()
    print('[*] get service info success')
    assert isinstance(s, dict)
    print(s)
    assert len(s) > 0
    
    
print('[2.5] 2.5 later call retrieve service')
reactor.callLater(2.5, test_service)


#
# shutdown function test
#
#----------------------------------------------------------------------
def stop():
    """"""
    print('[!] stop!')
    reactor.stop()

print('[5] 5 later stop')
reactor.callLater(5, stop)

print('[+] main loop')
reactor.run()