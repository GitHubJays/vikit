#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: run client for platform
  Created: 05/23/17
"""

from vikit.core.serviceadmin import serviceadmin_entity
from twisted.internet import reactor

sa = serviceadmin_entity.VikitServiceAdmin('testsa', '127.0.0.1', 7000)
sa.start()

reactor.run()