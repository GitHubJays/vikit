#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Error Action
  Created: 06/21/17
"""

from . import base
from . import ackbase

########################################################################
class VikitErrorAction(base.BaseAction, ackbase.Ackable):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, from_id, reason):
        """Constructor"""
        base.BaseAction.__init__(self)
        ackbase.Ackable.__init__(self)
        
        self.from_id = from_id
        self.reason = reason
        
    @property
    def id(self):
        """"""
        return self.from_id
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<VikitError: from:{} reason:{}>'.format(self.from_id, self.reason)
    
    
        
        
    
    