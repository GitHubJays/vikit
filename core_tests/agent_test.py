#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client Agent
  Created: 06/20/17
"""
import sys

sys.path.append('..')
from twisted.internet import reactor

from vikit.core.vikitclient import vikitagent

agent = vikitagent.VikitAgent('demo')
agent.add_service_addr('123123123', '127.0.0.1', 7034)

#----------------------------------------------------------------------
def execute_task():
    """"""
    print('execute')
    agent.execute(task_id='123123123123123', params={"target":'http://tbis.me',
                                                     'payload':'adfa',
                                                     'config':{'param1':True,
                                                               'param2':'asdfasd'}}) 
    agent.execute(task_id='12312323123123', params={"target":'http://tbis.me',
                                                     'payload':'adfa',
                                                     'config':{'param1':True,
                                                               'param2':'asdfasd'}}) 
    agent.execute(task_id='123123123123', params={"target":'http://tbis.me',
                                                     'payload':'adfa',
                                                     'config':{'param1':True,
                                                               'param2':'asdfasd'}}) 
    agent.execute(task_id='1223123123123', params={"target":'http://tbis.me',
                                                     'payload':'adfa',
                                                     'config':{'param1':True,
                                                               'param2':'asdfasd'}})     

#agent.remove_service()

#----------------------------------------------------------------------
def test(result):
    """"""
    print result
    
agent.regist_result_callback(test)

reactor.callLater(3, execute_task)

reactor.run()