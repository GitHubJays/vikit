#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: 
  Created: 05/22/17
"""

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

########################################################################
class CryptoBase(object):
    """"""



########################################################################
class DesCrypto(CryptoBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, key='a.a.a.a.aaaaaaaa'):
        """Constructor"""
        self._key = key
        
        self._mode = AES.MODE_CBC
        
        self._cryptor = AES.new(self._key, 
                                self._mode,
                                b'0000000000000000')
    
    #----------------------------------------------------------------------
    def enc(self, text):
        """"""
        #
        # fill until length == 16
        #
        length = 16
        count = len(text)
        if count < length:
            add = (length-count)
            #\0 backspace
            text = text + ('\0' * add)
        elif count > length:
            add = (length-(count % length))
            text = text + ('\0' * add)
            
        #
        # enc
        #
        self.ciphertext = self._cryptor.encrypt(text)
        
        #
        # to hex
        #
        return b2a_hex(self.ciphertext)        
        
    #----------------------------------------------------------------------
    def dec(self, text):
        """"""
        #
        # dec
        #
        plain_text  = self._cryptor.decrypt(a2b_hex(text))
        
        #
        # strip
        #
        return plain_text.rstrip('\0')    
    
    