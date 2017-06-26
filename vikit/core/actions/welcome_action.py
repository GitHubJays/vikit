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
class VikitWelcomeBase(object):
    """"""
    pass
    
    

########################################################################
class VikitWelcomeAction(base.BaseAction, ackbase.Ackable, VikitWelcomeBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        
        self.id = id
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<WelcomeAction from:{}>'.format(self.id)
    
########################################################################
class VikitClientWelcomeAction(base.BaseAction, ackbase.Ackable, VikitWelcomeBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        ackbase.Ackable.__init__(self)
        
        self.id = id
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<ClientWelcomeAction from:{}>'.format(self.id)
        
        
    
########################################################################
class VikitResultSubmitterWelcomeAction(base.BaseAction, ackbase.Ackable, VikitWelcomeBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id):
        """Constructor"""
        base.BaseAction.__init__(self)
        ackbase.Ackable.__init__(self)
        
        self.id = id
    
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return '<ResultSubbmitterWelcom from:{}>',format(self.id)
        
        
    
    
    
    