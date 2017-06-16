#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define VikitBase
  Created: 06/17/17
"""

from abc import ABCMeta, abstractmethod

########################################################################
class VikitBase(object):
    """"""
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def on_received_obj(self):
        """"""
        pass