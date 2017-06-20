#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Welcome
  Created: 06/17/17
"""

from . import base
from . import ackbase

########################################################################
class VikitWelcomeAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        
        self.id = id
        
    
    