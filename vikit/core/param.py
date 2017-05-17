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
        self._value_raw = value
        self._value = None
        self._set_value(self._value_raw)
    
    #----------------------------------------------------------------------
    def _set_value(self, value):
        """"""
        
        if value == None:
            self._value = None
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
            if self.type == TYPE_JSON:
                try:
                    json.loads(self._value_raw)
                    return True
                except:
                    return False 
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
        


########################################################################
class ParamSet(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        
        #
        # raw args
        #
        self._raw_args = args
        
        #
        # private info
        #
        self._param_map = {}
        self._dumped = {}
        self._kv = {}
        
        #
        # update
        #
        self._update(self._raw_args)
    
    #----------------------------------------------------------------------
    def _update(self, args):
        """"""
        _param_name_buffer = []
        
        def check_param(x):
            assert isinstance(x, Param), 'not a valid param! ' + \
                   'expect:Param but, got a {}'.format(str(type(x)))
            assert x.name not in _param_name_buffer, 'repeat parameter name(Param.name) !'
            _param_name_buffer.append(x.name)
            
            self._param_map[x.name] = x
            self._dumped[x.name] = {}
            self._dumped[x.name]['type'] = x.type
            self._dumped[x.name]['value'] = x.value
            self._dumped[x.name]['have_to'] = x.have_to
            
            self._kv[x.name] = x.value
            return x
            
        self._params = map(check_param, args)
    
    #----------------------------------------------------------------------
    def get_param_obj_by_name(self, name):
        """"""
        return self._param_map.get(name)
    
    #----------------------------------------------------------------------
    def get_param(self, name):
        """"""
        return self.get_param_obj_by_name(name)
    
    #----------------------------------------------------------------------
    def get_params(self):
        """"""
        return list(self._params)
    
    #----------------------------------------------------------------------
    def dumped(self):
        """"""
        return self._dumped
    
    #----------------------------------------------------------------------
    def now(self):
        """"""
        return self._kv
    
    #----------------------------------------------------------------------
    def get(self, name):
        """"""
        return self._kv.get(name)
    
    #----------------------------------------------------------------------
    def set(self, name, value):
        """"""
        _v = self.get_param(name)
        if _v:
            assert isinstance(_v, Param)
            _v.value = value
        
        self._update(self._raw_args)
    
    #----------------------------------------------------------------------
    def has_key(self, key):
        """"""
        return self._kv.has_key(key)
    
    #
    # check prepared
    #
    #----------------------------------------------------------------------
    def check(self):
        """"""
        _buff = list(filter(lambda x: not x.check(), self.get_params()))
        if _buff == []:
            return True, _buff
        else:
            return False, _buff
        
        
        
        
        
        
        
    
    