#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Ack Base
  Created: 06/17/17
"""

from ..utils import getuuid

########################################################################
class Ackable(object):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        self.token = getuuid()
        

########################################################################
class Ack(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, token):
        """"""
        self.token = token
