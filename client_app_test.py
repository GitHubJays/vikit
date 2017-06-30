#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client Test
  Created: 06/24/17
"""

from twisted.internet import reactor

from vikit.apps import twisteduserclient
from vikit import api

#----------------------------------------------------------------------
def test_app():
    """"""
        
    c = twisteduserclient.TwistedClient()
    c.start()
    
    #----------------------------------------------------------------------
    def execute_task1():
        """"""
        global c
    
        c.execute('demo', {"target":'http://tbis.me',
                           'payload':'adfa',
                           'config':{'param1':True,
                                     'param2':'asdfasd'}}, offline=True)
    
    #----------------------------------------------------------------------
    def execute_task2():
        """"""
        
        c.execute('demo', {"target":'http://tbis.me',
                           'payload':'adfa',
                           'config':{'param1':True,
                                     'param2':'asdfasd'}}, offline=True)   
    
    #reactor.callLater(1, execute_task1)
    
    reactor.callLater(3, execute_task2)
    c.mainloop_start()
    
#----------------------------------------------------------------------
def test_api():
    """"""
    api.client.twisted_start_client()
    reactor.callLater(3, api.client.execute, 'demo', {"target":'http://tbis.me',
                           'payload':'adfa',
                           'config':{'param1':True,
                                     'param2':'asdfasd'}})
    def print_info():
        print(api.client.get_available_modules())
        print(api.client.get_help_for_module('demo'))
    reactor.callLater(2, print_info)
    api.client.mainloop_start()
    
test_api()