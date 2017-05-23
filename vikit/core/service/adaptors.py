#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Adatpr
  Created: 05/22/17
"""

########################################################################
class AdaptorBase(object):
    """"""

    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        raise NotImplemented()
    
    #----------------------------------------------------------------------
    def recv(self, obj):
        """"""
        raise NotImplemented()
    

########################################################################
class TwistedAdaptor(AdaptorBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, twisted_conn, ):
        """Constructor"""
        
        self._twisted_conn = twisted_conn
    
    #----------------------------------------------------------------------
    def send(self, obj):
        """"""
        text = compact(obj)
    
        self._twisted_conn.transport.write()