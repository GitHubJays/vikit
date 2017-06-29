#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client Test
  Created: 06/24/17
"""

from twisted.internet import reactor

from vikit.apps import twisteduserclient

c = twisteduserclient.TwistedClient()
c.start()

#----------------------------------------------------------------------
def execute_task():
    """"""
    global c

    c.execute('demo', {"target":'http://tbis.me',
                       'payload':'adfa',
                       'config':{'param1':True,
                                 'param2':'asdfasd'}}, offline=True)
    c.execute('demo', {"target":'http://tbis.me',
                       'payload':'adfa',
                       'config':{'param1':True,
                                 'param2':'asdfasd'}})   

reactor.callLater(5, execute_task)

c.mainloop_start()