#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: run client for platform
  Created: 05/23/17
"""

from vikit.core.service import vservice
from twisted.internet import reactor

sadmin = vservice.VServiceAdmin(name='test', control_host='127.0.0.1', control_port=7001)

sadmin.serve()

sadmin.start_new_service(service_name='demo', module_name='demo', bind_port=7004, bind_if='')

reactor.callLater(5, sadmin.stop_service_by_name, *('demo',))
reactor.callLater(8, sadmin.stop_serve)
reactor.callLater(8, reactor.stop)

reactor.run()