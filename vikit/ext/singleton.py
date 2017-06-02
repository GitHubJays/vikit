#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Singleton
  Created: 06/02/17
"""

########################################################################
class Singleton(object):
    """"""

    #----------------------------------------------------------------------
    def __new__(self, *v, **kw):
        """"""
        if not hasattr(self, '_instance'):
            orig = super(Singleton, self)
            self._instance = orig.__new__(self, *v, **kw)
        
        return self._instance