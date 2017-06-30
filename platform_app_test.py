#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test For TwistedPlatform
  Created: 06/23/17
"""

from vikit.apps import twistedplatform

config = twistedplatform.PlatformConfig()
p = twistedplatform.TwistedPlatform('thisisaplatform_id', config=config)
p.add_default_service('demo', 7034)
#p.add_default_service('demo', 7035)
#p.add_default_service('demo', 7036)
#p.add_default_service('demo', 7037)
p.start()


p.mainloop_start()