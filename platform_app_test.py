#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test For TwistedPlatform
  Created: 06/23/17
"""
import time

from twisted.internet import reactor
from vikit.apps import twistedplatform
from multiprocessing import Process
from threading import Thread

config = twistedplatform.PlatformConfig()
p = twistedplatform.TwistedPlatform('thisisaplatform_id', config=config)

p.start()
p.add_default_service('demo', 7034)
p.add_default_service('demo', 7035)
p.add_default_service('demo', 7036)
p.add_default_service('demo', 7037)

#p.mainloop_start()
#pr = Thread(target=p.mainloop_start)
#pr.start()


print('tset')

#----------------------------------------------------------------------
def test_print_info():
    """"""
    
    print('start service')
    print(p.get_service_nodes())
    print(p.get_services())
    print(p.get_services_info())
    print(p.get_service_nodes_info())


reactor.callLater(5, test_print_info)


p.mainloop_start()
