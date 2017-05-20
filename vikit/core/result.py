#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Result
  Created: 05/20/17
"""

import types

from . import target

########################################################################
class Result:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, dict_obj):
        """Constructor"""
        assert isinstance(dict_obj, dict)
        self._dict_obj = dict_obj
        
        self._traveller = _DictTrav(dict_obj)
        
        self._target_buff = []
        
        self._remove_repeat = set()
    
    #----------------------------------------------------------------------
    def _pick_up_targets(self, parent, key, value, depth):
        """"""
        #
        # check key/value/parent
        #
        def pick_up_targets(val):
            if val in self._remove_repeat:
                return
            
            _ = target.Target(target=val, type=target.TYPE_AUTO, name='target')
            
            if _.type == target.TYPE_RAW:
                try:
                    _ = target.Target(target, type=target.TYPE_NETLOC, name='target')
                except AssertionError as e:
                    _ = None
            
            if _:
                self._target_buff.append(_)
        
        
        def checkit(t):
            if isinstance(t, types.StringTypes):
                pick_up_targets(t)
            elif isinstance(t, (types.ListType, types.TupleType)):
                for i in t:
                    checkit(t)
            else:
                pick_up_targets(str(t))


########################################################################
class _DictTrav(object):
    """
    Go through the dict, and read every 
    
    Attributes:
    
    dict_obj: :dict:
    """
    ROOT_NODE = 'ROOT'

    #----------------------------------------------------------------------
    def __init__(self, dict_obj, handler=None):
        """Constructor"""
        assert isinstance(dict_obj, dict)
        self._orig = dict_obj
        
        # 
        # set leaf node handle
        #
        if handler:
            assert callable(handler)
            self._handler = handler
        else:
            self._handler = None
            
        self._init_stack()
        
        self.depth_table = {}
    
    #----------------------------------------------------------------------
    def _init_stack(self):
        """"""
        self._stack = []
        self._stack.append(self.ROOT_NODE)
        
    @property
    def current_parent(self):
        """"""
        return self._stack[-1]
    
    
    #----------------------------------------------------------------------
    def gothrough_dict(self):
        """"""
        self._init_stack()
        
        #
        # start go through
        #
        self._travel(self._orig)
        
    #----------------------------------------------------------------------
    def _travel(self, _dict):
        """"""
        assert isinstance(_dict, dict)
        for i in _dict.iteritems():
            key = i[0]
            val = i[1]
            
            if isinstance(val, dict):
                #print('   ' * self.depth + "+-{}".format(repr(key)))
                self._stack.append(key)
                self._travel(val)
            else:
                #print('   ' * self.depth + '|-' + ' {}=>{}'.format(repr(key), repr(val)))
                self._travel_leaf(self.current_parent, key, val, depth=self.depth)
        
        _ = self._stack.pop()
        if _ == self.ROOT_NODE:
            self._init_stack()
    
    #----------------------------------------------------------------------
    @property
    def depth(self):
        """"""
        return len(self._stack) 
    
    #----------------------------------------------------------------------
    def _travel_leaf(self, parent, key, value, depth):
        """"""
        if not self.depth_table.has_key(self.depth):
            self.depth_table[self.depth] = {}
        
        if not self.depth_table.get(self.depth).has_key(parent):
            self.depth_table.get(self.depth)[parent] = []
            
        self.depth_table[self.depth].get(parent).append((key, value))
        
        
        
        if self._handler:
            self._handler(parent, key, value, depth)

