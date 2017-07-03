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


#----------------------------------------------------------------------
def print_task_id(result_dict):
    """"""
    print('[trigger]: got a task! ID:{}'.format(result_dict.get('task_id')))
    return result_dict

ctrigger = get_client_proxy(platform_host='39.108.169.134', platform_port=7000,
                            id=None)
ctrigger.regist_result_callback(print_task_id)

while not ctrigger.state == state_CONNECTED:
    pass

modules = ctrigger.get_available_modules()
print(ctrigger.get_help_for_module('demo'))

print('submit task')
ctrigger.execute('demo', {"target":'http://tbis.me',
                          'payload':'adfa',
                          'config':{'param1':True,
                                    'param2':'asdfasd'}},
                 offline=True)

ctrigger.execute('demo', {"target":'http://tbis.me',
                          'payload':'adfa',
                          'config':{'param1':True,
                                    'param2':'asdfasd'}},
                 True)

print('submit task success')

print('sleeping 10 seconds')
time.sleep(10)
ctrigger.shutdown()
exit()
