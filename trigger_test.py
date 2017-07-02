#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: 
  Created: 07/02/17
"""
import time

import unittest
from vikit.api.trigger import get_client_proxy
from vikit.api.client import state_CONNECTED


ctrigger = get_client_proxy(platform_host='127.0.0.1', platform_port=7000,
                            id=None)

modules = ctrigger.get_available_modules()
print(ctrigger.get_help_for_module('demo'))
#assert len(modules) > 0
print('submit task')
ctrigger.execute('demo', {"target":'http://tbis.me',
                          'payload':'adfa',
                          'config':{'param1':True,
                                    'param2':'asdfasd'}},
                 False, offline=True)
print('submit task success')

print('sleeping 10 seconds')
time.sleep(20)
ctrigger.shutdown()
exit()
