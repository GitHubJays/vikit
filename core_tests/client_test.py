#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: run client for platform
  Created: 05/23/17
"""

import time
import sys

sys.path.append('..')

from twisted.internet import reactor    
from vikit.core.vikitclient import vikitclient
from vikit.core.launch.twistedlaunch import TwistdConnector
from vikit.core.eventemitter import twistedemitter

vc = vikitclient.VikitClient('test')

conn = TwistdConnector(vc)

conn.connect('127.0.0.1', 7034)

emitter = twistedemitter.TwistedClientEventEmitter(conn)

#time.sleep(1)

#----------------------------------------------------------------------
def test():
    """"""
    print('test called!')
    emitter.execute('demoid', {"target":'http://tbis.me',
                               'payload':'adfa',
                               'config':{'param1':True,
                                         'param2':'asdfasd'}})
    emitter.execute('demoissd', {"target":'http://tbis.me',
                               'payload':'adfa',
                               'config':{'param1':True,
                                         'param2':'asdfasd'}})    
    
    

print('call test 2s later')
reactor.callLater(2, test)

#----------------------------------------------------------------------
def stop_client():
    """"""
    conn.stop()
    

#reactor.callLater(6, stop_client)



reactor.run()

