#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Persist data
  Created: 05/18/17
"""

from __future__ import unicode_literals

import bsddb185
import types

########################################################################
class KVPersister(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, db_path):
        """Constructor"""
        self._bdb = bsddb185.btopen(db_path, 'c')
        
        
    #----------------------------------------------------------------------
    def set(self, key, value):
        """"""
        assert isinstance(key, types.StringTypes) and \
               isinstance(value, types.StringTypes), 'key and value must be a str/unicode'

        self._bdb[key] = value

    #----------------------------------------------------------------------
    def get(self, key):
        """"""
        try:
            return self._bdb[key]
        except KeyError as e:
            return None
    
    #----------------------------------------------------------------------
    def has_key(self, key):
        """"""
        return self._bdb.has_key(key)
    
    #----------------------------------------------------------------------
    def delete(self, key):
        """"""
        if self.has_key(key):
            del self._bdb[key]
            return True
        else:
            return False
    
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self._bdb.close()
        
    