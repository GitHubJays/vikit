#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Start Platform
  Created: 06/11/17
"""

from twisted.internet import reactor
from vikit.core.platform import platform_entity

pl = platform_entity.Platform(id='testplatform')
pl.serve()

reactor.run()