#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define VikitBase
  Created: 06/17/17
"""

import time
from abc import ABCMeta, abstractmethod

########################################################################
class VikitBase(object):
    """"""
    
    __metaclass__ = ABCMeta
    
    disable_default_connectionMade = False
    
    _dict_record_sender = {}

    @abstractmethod
    def on_received_obj(self):
        """"""
        pass
    
    @abstractmethod
    def on_connection_made(self, *vargs, **kw):
        """"""
        pass
    
    @abstractmethod
    def on_connection_lost(self, *vargs, **kw):
        """"""
        pass
    
    #@abstractmethod
    def get_sender(self, id, default=None):
        """"""
        return self._dict_record_sender.get(id, default)
    
    #@abstractmethod
    def regist_sender(self, sender, id=None):
        """"""
        if self._dict_record_sender.has_key(id):
            pass
        else:
            self._dict_record_sender[id] = sender
        