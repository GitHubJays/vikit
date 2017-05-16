#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: core target
  Created: 05/16/17
"""

from __future__ import unicode_literals

import types
import os

from g3ar.utils import verify_utils
from g3ar import DictParserFromIter


#
# DEFINE TYPE
#
TYPE_IPV4 = 'ipv4'
TYPE_IPV6 = 'ipv6'
TYPE_NETLOC = 'netloc'
TYPE_URL = 'url'
TYPE_RAW = 'raw'
TYPE_AUTO = 'auto'
TYPE_FILE = 'file'
TYPE_DOMAIN = 'domain'

TYPES = [TYPE_IPV4, TYPE_IPV6, \
         TYPE_FILE, \
         TYPE_AUTO, \
         TYPE_NETLOC, \
         TYPE_RAW, \
         TYPE_URL, \
         TYPE_DOMAIN,]

########################################################################
class TargetEnum(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, targets, type):
        """Constructor"""
        assert type in TYPES, 'not a valid type'
        assert type != TYPE_AUTO, 'cannot be TYPE_AUTO'
        assert isinstance(targets, (types.ListType, \
                                    types.TupleType)), 'targets should be' + \
                                    'list/tuple'
        
        self._raw = list(targets)
        _nbuff = -1
        
        if type == TYPE_IPV4:
            _nbuff = len(filter(verify_utils.is_ipv4, self._raw))
        elif type == TYPE_DOMAIN:
            _nbuff = len(filter(verify_utils.is_domain, self._raw))
        elif type == TYPE_IPV6:
            _nbuff = len(filter(verify_utils.is_ipv6, self._raw))
        elif type == TYPE_NETLOC:
            def _verfify_netloc(x):
                _ = x.split(':')
                _net = _[0]
                _port = _[1]
                try:
                    assert verify_utils.is_ipv4(_net) or \
                           verify_utils.is_ipv6(_net) or \
                           verify_utils.is_domain(_net), 'netlocation error: {}'.format(x)
                    assert int(_port) >= 0, 'netlocation.port error! port: {}'.format(_port)
                    return True
                except AssertionError:
                    return False
            _nbuff = len(filter(_verfify_netloc, self._raw))
        elif type == TYPE_URL:
            _nbuff = len(filter(verify_utils.is_url, self._raw))
        elif type == TYPE_FILE:
            def _check_file(x):
                if os.path.exists(x):
                    pass
                else:
                    raise AssertionError('no such file : {}'.format(x))
            
            map(_check_file, self._raw)
            _nbuff = len(self._raw)
        elif type == TYPE_RAW:
            _nbuff = len(self._raw)
        
        assert _nbuff == len(self._raw), 'some target invalid'
        
        self._iter = iter(self._raw)
        self._type = type
        
    #----------------------------------------------------------------------
    def __iter__(self):
        """"""
        return self._iter
    
    #----------------------------------------------------------------------
    def reset(self):
        """"""
        self._iter = iter(self._raw)
        
    @property
    def type(self):
        """"""
        return self._type
    
    #----------------------------------------------------------------------
    def all(self):
        """"""
        return self._raw
        
        

########################################################################
class Target(TargetEnum):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, target, type):
        """Constructor"""
        self._target = target
        
        if type == TYPE_AUTO:
            if verify_utils.is_ipv4(self._target):
                type = TYPE_IPV4
            elif verify_utils.is_ipv6(self._target):
                type = TYPE_IPV6
            elif verify_utils.is_url(self._target):
                type = TYPE_URL
            elif verify_utils.is_domain(self._target):
                type = TYPE_DOMAIN
            elif os.path.exists(self._target):
                type = TYPE_FILE
            else:
                type = TYPE_RAW
        
        TargetEnum.__init__(self, targets=list([self._target]), type=type)
    
    @property
    def data(self):
        """"""
        return self._target
        
    
    