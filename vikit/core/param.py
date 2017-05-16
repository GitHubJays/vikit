#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Param For Mod
  Created: 05/17/17
"""

from __future__ import unicode_literals

import types
import json

#
# DEFINE PARAM
#
TYPE_JSON = 'json'
TYPE_INT = 'int'
TYPE_STR = 'str'
TYPE_BOOL = 'bool'
TYPE_FLOAT = 'float'
TYPE_ENUM = 'enum'
TYPE_BYTES = 'bytes'

_PARAM_TYPE_BASIC_MAP = {
    TYPE_INT : types.IntType,
    TYPE_FLOAT : types.FloatType,
    TYPE_STR : types.UnicodeType,
    TYPE_BOOL : types.BooleanType,
    TYPE_ENUM : types.ListType,
    TYPE_BYTES : type(b'\xff\xff\xff')
}

TYPES = [TYPE_JSON, TYPE_ENUM, \
         TYPE_FLOAT, TYPE_INT, \
         TYPE_BOOL, TYPE_STR,
         TYPE_BYTES]


########################################################################
class ParamError(Exception):
    """"""
   

########################################################################
class Param(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, value=None, type=TYPE_STR, have_to=True):
        """Constructor"""
        #
        # set name
        #
        self._name = name
        
        #
        # set have to
        #
        self._have_to = bool(have_to)
        
        #
        # set type
        #
        assert type in TYPES, 'unknown type in param type'
        self._type = type
        
        #
        # set value and check value
        #
        self._value = None
        self._set_value(value)
    
    #----------------------------------------------------------------------
    def _set_value(self, value):
        """"""
        
        if value == None:
            pass
        else:
            if self._type != TYPE_JSON:
                if isinstance(value, _PARAM_TYPE_BASIC_MAP[self._type]):
                    self._value = value
                else:
                    try:
                        self._value = _PARAM_TYPE_BASIC_MAP[self._type](value)
                    except Exception as e:
                        raise ParamError('the value cannot match the type!' + \
                                         ' value:{} type:{} error_message:{}'\
                                         .format(str(value), str(self._type), e.message))
            else:
                try:
                    self._value = json.loads(value)
                except Exception as e:
                    raise ParamError('the json.loads error! value:{} error_message:{}'\
                                     .format(str(value), e.message))
                else:
                    pass
                
    
    #----------------------------------------------------------------------
    @property
    def name(self):
        """"""
        return self._name
    
    #----------------------------------------------------------------------
    def check(self):
        """"""
        if self.value == None:
            if self.have_to:
                return False
            else:
                return True
        else:
            return isinstance(self.value, _PARAM_TYPE_BASIC_MAP[self.type])
    
    @property
    def value(self):
        """"""
        return self._value
    
    @value.setter
    def value(self, value):
        """"""
        self._set_value(value)
    
    @property
    def type(self):
        """"""
        return self._type
    
    @property
    def have_to(self):
        """"""
        return self._have_to
        

                