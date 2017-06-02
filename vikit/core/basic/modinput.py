#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Control Mod Input
  Created: 05/17/17
"""

import warnings

from . import payload

from .param import Param, ParamSet
from .payload import PayloadEnum, Payload
from .target import TargetEnum, Target
from .mixer import mixer

########################################################################
class NoMatchedValue(Exception):
    """"""
    pass
    

########################################################################
class DemandBase(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, dst, dst_type=None):
        """Constructor"""
        
        self._dst = dst
        self._dst_type = dst_type
        
        self._value = None
    
    @property
    def dst(self):
        """"""
        return self._dst
    
    @property
    def dst_type(self):
        """"""
        return self._dst_type
    
    #----------------------------------------------------------------------
    def match(self, obj):
        """"""
        assert self.dst == obj.name, 'dst cannot match name'
        
        if self.dst_type:
            assert self.dst_type == obj.type
        
        self._value = obj
    
    #----------------------------------------------------------------------
    def check(self, stricted=True):
        """"""
        if self._value:
            return self._value.check()
        else:
            if stricted:
                raise NoMatchedValue('current demand:{} need to match a value'\
                                     .format(self.dst))
            else:
                return False
    
    @property
    def value(self):
        """"""
        if self._value:
            return self._value
        else:
            raise NoMatchedValue('current demand:{} need to match a value'\
                                 .format(self.dst))

########################################################################
class TargetDemand(DemandBase):
    """"""

########################################################################
class PayloadDemand(DemandBase):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, dst, dst_type=payload.TYPE_TEXT):
        """"""
        DemandBase.__init__(self, dst, dst_type)
        


########################################################################
class ParamDemand(DemandBase):
    """"""
    
    #----------------------------------------------------------------------
    def __init__(self, dst, dst_type, have_to=True):
        """"""
        self._haveto = have_to
        
        DemandBase.__init__(self, dst, dst_type)
    
    @property
    def have_to(self):
        """"""
        return self._haveto
    
    

########################################################################
class _Demands(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        self._d_targets = filter(lambda x: isinstance(x, TargetDemand), args)
        self._d_params = filter(lambda x: isinstance(x, ParamDemand), args)
        self._d_payloads = filter(lambda x: isinstance(x, PayloadDemand), args)
        
        #
        # build map
        #
        self._map = {}
        self._map['config'] = {}
        for i in args:
            if isinstance(i, ParamDemand):
                self._map['config'][i.dst] = i
            else:
                self._map[i.dst] = i
    
    #----------------------------------------------------------------------
    def get(self, key):
        """"""
        _r = self._map.get(key)
        if _r:
            return _r
        else:
            return self._map['config'].get(key)
    
    #----------------------------------------------------------------------
    def get_target(self, key='target'):
        """"""
        _r = self._map.get(key)
        if _r in self._d_targets:
            return _r
        else:
            return None
    
    #----------------------------------------------------------------------
    def get_param(self, key):
        """"""
        if self._map.has_key('config'):
            _r = self._map['config'].get(key)
            if _r in self._d_params:
                return _r
            else:
                return None
        else:
            return None
    
    #----------------------------------------------------------------------
    def get_payload(self, key):
        """"""
        _r = self._map.get(key)
        if _r in self._d_payloads:
            return _r
        else:
            return None
        
    #----------------------------------------------------------------------
    def has_target(self, key='target'):
        """"""
        #
        # check target by order
        #
        for i in self._d_targets:
            if i.name == 'target':
                return True
            else:
                pass
        return False
    
    #----------------------------------------------------------------------
    def has_payload(self, key='payload'):
        """"""
        #
        # check payload
        #
        for i in self._d_payloads:
            if i.name == 'payload':
                return True
            else:
                pass
        
        return False
    
    #----------------------------------------------------------------------
    def has_param(self, key):
        """"""
        #
        # check param
        #
        for i in self._d_params:
            if i.name == key:
                return True
            else:
                pass
        
        return False
    
    #----------------------------------------------------------------------
    def match(self, *args):
        """"""
        state = False
        unsets = []
        
        for obj in args:
            _dst = obj.name
            
            if isinstance(obj, Param):
                _demand = self._map['config'].get(_dst)
            else:
                _demand = self._map.get(_dst)
            
            if _demand:
                assert isinstance(_demand, DemandBase)
                
                if _demand:
                    try:
                        _demand.match(obj)
                    except NoMatchedValue as e:
                        unsets.append(_demand)
                else:
                    pass
            else:
                pass
        
        if unsets == []:
            state = True
            return state, unsets
        else:
            state = False
            return state, unsets
        
    #----------------------------------------------------------------------
    def check(self, restricted=False):
        """"""
        state = False
        unsets = []
        
        for i in self._map.values():
            if isinstance(i, dict):
                for j in i.values():
                    if j.check(restricted):
                        pass
                    else:
                        unsets.append(j)
            else:
                if i.check(restricted):
                    pass
                else:
                    unsets.append(i)
        
        if unsets == []:
            return True, unsets
        else:
            return False, unsets  


########################################################################
class ModInput(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, *args):
        """Constructor"""
        #
        # set demands
        #
        self._demands = _Demands(*args)

        #
        # init dst
        #
        self._targets = []
        self._params = []
        self._paramset = None
        self._payloads = []
        
        #
        # target and payload
        #
        self._target_payload_maps = {}
        
        #
        # config
        #
        self._mixer_gen = None
    
    #----------------------------------------------------------------------
    def check(self, restricted=False):
        """"""
        #
        # check targets
        #
        return self._demands.check(restricted)
    
    #----------------------------------------------------------------------
    def match(self, *args):
        """"""
        _ret = self._demands.match(*args)
        
        for i in args:
            if isinstance(i, (Target, TargetEnum)):
                assert not self._target_payload_maps.has_key(i.name)
                self._targets.append(i)
                self._target_payload_maps[i.name] = i
            elif isinstance(i, (Payload, PayloadEnum)):
                assert not self._target_payload_maps.has_key(i.name)
                self._payloads.append(i)                
                self._target_payload_maps[i.name] = i
            elif isinstance(i, Param):
                self._params.append(i)
        
        self._paramset = ParamSet(*tuple(self._params))
        
        self._mixer_gen = mixer(*tuple(self._target_payload_maps.values()))

        return _ret

    @property
    def targets(self):
        """"""
        return self._targets
    
    @property
    def payloads(self):
        """"""
        return self._payloads
    
    @property
    def paramset(self):
        """"""
        return self._paramset

    @property
    def config(self):
        """"""
        return self._paramset.now()
    
    #----------------------------------------------------------------------
    def __iter__(self):
        """"""
        return self
    
    #----------------------------------------------------------------------
    def next(self):
        """"""
        data = {}
        data['config'] = self.config
        
        i = self._mixer_gen.next()
        for _index in range(len(i)):
            data[self._target_payload_maps.keys()[_index]] = i[_index]
    
        return data
    
    #----------------------------------------------------------------------
    def reset(self):
        """"""
        map(lambda x: x.reset(), self._target_payload_maps.values())
        self._mixer_gen = mixer(*tuple(self._target_payload_maps.values()))
        
        
    #----------------------------------------------------------------------
    def check_from_dict(self, dict_params, stricted=True):
        """"""
        _cf = dict_params.get('config')
        if _cf:
            assert isinstance(_cf, dict)
        
        #
        # check target / payload
        #
        for i in dict_params.iteritems():
            key = i[0]
            value = i[1]
            
            if key == 'config':
                pass
            else:
                _d = self._demands.get(key)
                if _d:
                    if isinstance(_d, TargetDemand):
                        
                        _t = Target(target=value, type=_d.dst_type, name=key)
                        _d.match(_t)
                    elif isinstance(_d, PayloadDemand):
                        _p = Payload(value, _d.dst_type, key)
                        _d.match(_p)
                    else:
                        raise AssertionError('no target or payload found!')
                else:
                    warnings.warn('no such param key:{} in demands!'.format(key))
        
        #
        # check params(config)
        #
        if _cf:
            for i in _cf.iteritems():
                key = i[0]
                value = i[1]
                
                _d = self._demands.get_param(key)
                if _d:
                    if isinstance(_d, ParamDemand):
                        _p = Param(key, value, _d.dst_type, _d.have_to)
                        _d.match(_p)
                        assert _p.check(), 'param checked error'
                    else:
                        warnings.warn('no param found!')
                else:
                    msg = 'no such param key:{} in demands!'.format(key)
                    warnings.warn(msg)
        return dict_params
        
                    
        
        
        
        