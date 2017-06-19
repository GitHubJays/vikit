#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4>
  Purpose: 
  Created: 06/19/17
"""

import time
from twisted.internet import reactor

from vikit.core.platform import vikitplatform
from vikit.core.launch import twistedbase
from vikit.core.launch.twistedlaunch import TwistdLauncher
from vikit.core.eventemitter import twistedemitter

p = vikitplatform.VikitPlatform('platform')
l = TwistdLauncher(p)
l.serve(port=7000, net_if='')


#----------------------------------------------------------------------
def _start_service():
    """"""
    pass

reactor.run()
