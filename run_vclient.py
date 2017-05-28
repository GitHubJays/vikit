#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: run client for test
  Created: 05/27/17
"""

import time

from twisted.internet import reactor
from twisted.internet.defer import Deferred

from vikit.core.service import client 


vargs = ({'target':'http://tbis.me',
          'payload':'data',
          'config':{
              'param1':True,
              'param2':'aaaa'
              }},)

vclient = client.VClient(rhost='127.0.0.1', rport=7004)
vclient.connect()

reactor.callLater(5, vclient.execute, *vargs)
reactor.run()


