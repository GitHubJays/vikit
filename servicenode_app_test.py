#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test For TwistedServiceNode
  Created: 06/23/17
"""

from vikit.apps import twistedservicenode

config = twistedservicenode.ServiceNodeConfig(platform_host='127.0.0.1',
                                              platform_port=7000)

sn = twistedservicenode.TwistedServiceNode(id='testnode', config=config)
sn.start()

sn.mainloop_start()


