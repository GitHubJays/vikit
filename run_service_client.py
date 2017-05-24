#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: run client for platform
  Created: 05/23/17
"""

from vikit.core.service import vservice

vserver = vservice.VService(module_name=None, control_host='127.0.0.1', control_port=7001, 
                           bind_port=7003)
vserver.serve()