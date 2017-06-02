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
class Result(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, dict_obj, restricted_node_names=['no_targets',]):
        """Constructor"""
        assert isinstance(dict_obj, dict)
        self._dict_obj = dict_obj
        
        self._target_buff = []
        
        self._remove_repeat = set()
        
        assert isinstance(restricted_node_names, list), 'restricted nodes should be a list!'
        self._restrict_nodes = [] + restricted_node_names
    
    #----------------------------------------------------------------------
    def _pick_up_targets(self, parent, key, value, depth):
        """"""
        #
        # check key/value/parent
        #
        def pick_up_targets(val):
            if val in self._remove_repeat:
                return
            else:
                self._remove_repeat.add(val)
            
            
            _ = target.Target(target=val, type=target.TYPE_AUTO, name='target')
            
            if _.type == target.TYPE_RAW:
                try:
                    _ = target.Target(target=val, type=target.TYPE_NETLOC, name='target')
                except AssertionError as e:
                    _ = None
            else:
                self._target_buff.append(_)
        
        
        def checkit(t):
            if isinstance(t, types.StringTypes):
                pick_up_targets(t)
            elif isinstance(t, (types.ListType, types.TupleType)):
                for i in t:
                    checkit(i)
            else:
                pick_up_targets(str(t))

        #
        # parent checking
        #
        try:
            checkit(parent)
        except AssertionError as e:
            pass
        #
        # key checking
        #
        try:
            checkit(key)
        except AssertionError as e:
            pass
        
        #
        # value checking
        #
        try:
            checkit(value)
        except AssertionError as e:
            pass
            
    #----------------------------------------------------------------------
    def extract_targets(self):
        """"""
        self._traveller = _DictTrav(self._dict_obj, handler=self._check_node)
        self._traveller.gothrough_dict()
        
        return self._target_buff

    #----------------------------------------------------------------------
    def _check_node(self, parent, key, value, depth):
        """"""
        if parent in self._restrict_nodes:
            pass
        elif key in self._restrict_nodes:
            pass
        else:
            self._pick_up_targets(parent, key, value, depth)
            
    
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

