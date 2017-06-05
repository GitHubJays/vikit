#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform Client For Service Admin
  Created: 06/04/17
"""

from ..common import baseprotocol
from ..basic.crypto import CryptoBase
from ..basic import serializer


########################################################################
class PlatformClientProtocolForServiceAdmin(baseprotocol.VikitProtocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, cryptor, *args, **kw):
        """Constructor"""
        self._cryptor = cryptor
        assert isinstance(self._cryptor, CryptoBase)
        baseprotocol.VikitProtocol.__init__(self, *args, **kw)
    
    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        assert isinstance(self, serializer.Serializer)
        self.serializer.set
        
        
    
    