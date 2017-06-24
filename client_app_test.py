#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client Test
  Created: 06/24/17
"""

from vikit.apps import twisteduserclient

c = twisteduserclient.TwistedClient()
c.start()

c.mainloop_start()