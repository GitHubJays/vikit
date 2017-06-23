#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Agent Pool Test
  Created: 06/21/17
"""

import time
import sys

sys.path.append('..')

from twisted.internet import reactor

from vikit.core.vikitclient import vikitagentpool
from vikit.core.vikitdatas import vikittaskfeedback
from vikit.core.launch import twistedlaunch
from vikit.core.eventemitter import twistedemitter

pool = vikitagentpool.VikitClientAgentPool(id='test')
connector = twistedlaunch.TwistdConnector(pool)
connector.connect('127.0.0.1', 7000)

emitter = twistedemitter.TwistdClientAgentPoolEmitter(connector)


#----------------------------------------------------------------------
def _start_update():
    """"""
    print(pool._dict_record_sender)
    emitter.start_update_services()
    
reactor.callLater(3, _start_update)
    
#----------------------------------------------------------------------
def _start_get_services():
    """"""
    
    print emitter.get_service()   

reactor.callLater(4, _start_get_services)

#----------------------------------------------------------------------
def _execute_tasks():
    """"""
    module_name = 'demo'
    task_id = 'taskdemoteataeasdtasd'
    params = {"target":'http://tbis.me',
              'payload':'adfa',
              'config':{'param1':True,
                        'param2':'asdfasd'}}
    result = emitter.execute(module_name=module_name, \
                             task_id=task_id, \
                             params=params, 
                             service_id=None,)
    
    assert isinstance(result, vikittaskfeedback.VikitTaskFeedback)
    assert result.state
    
#reactor.callLater(4, _execute_tasks)
reactor.run()