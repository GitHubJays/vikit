#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Serializer
  Created: 05/22/17
"""

import pickle
import zlib
import base64

from . import crypto

########################################################################
class Serializer(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, crypto_obj=None):
        """Constructor"""

        assert crypto_obj == None or \
               isinstance(crypto_obj, crypto.CryptoBase)

        self._cryptor = crypto_obj

    #----------------------------------------------------------------------
    def set_cryptor(self, obj=None):
        """"""
        if obj:
            assert isinstance(obj, crypto.CryptoBase)

        self._cryptor = obj

    #----------------------------------------------------------------------
    def serialize(self, obj):
        """"""
        #
        # pickle obj
        #
        pickle_str = pickle.dumps(obj)

        #
        # zlib compress
        #
        cp = zlib.compress(pickle_str)

        #
        # base64
        #
        text = base64.b64encode(cp)

        #
        # enc
        #
        if self._cryptor:
            text = self._cryptor.enc(text)

        return text

    #----------------------------------------------------------------------
    def unserialize(self, text):
        """"""
        #
        # dec
        #
        if self._cryptor:
            text = self._cryptor.dec(text)

        #
        # base64 dec
        #
        text = base64.b64decode(text)

        #
        # zlib decompress
        #
        raw = zlib.decompress(text)

        #
        # pickle loads
        #
        obj = pickle.loads(raw)

        return obj

_serializer = Serializer()

#----------------------------------------------------------------------
def get_serializer(cryptor=None):
    """"""
    if cryptor:
        return Serializer(cryptor)
    else:
        return _serializer



