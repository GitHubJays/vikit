#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define EmitterBase
  Created: 06/17/17
"""

from abc import ABCMeta

from ..launch.interfaces import LaunchableIf

########################################################################
class EmitterBase(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, launcher):
        """Constructor"""
        assert isinstance(launcher, LaunchableIf)
        self.launcher = launcher
    