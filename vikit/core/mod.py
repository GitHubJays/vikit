#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Mod Define
  Created: 05/17/17
"""

from __future__ import unicode_literals

import queue
import time
import types
import os
 
from g3ar import ThreadPoolX

#
# DEFINE PRIVATE VAR
#
_CURRENT_PATH = os.path.dirname(__file__)
_DEFAULT_DATAS_PATH_R = '../datas/'
_DEFAULT_DATAS_PATH = os.path.join(_CURRENT_PATH, _DEFAULT_DATAS_PATH_R)

#
# define keywords
#
NAME = 'NAME' # mod name

AUTHOR = 'AUTHOR' # mod author 
DESCRIPTION = 'DESCRIPTION' # mod description
RESULT_DESC = 'RESULT_DESC' # return of the result

# demands
INPUT = 'DEMANDS' 
INPUT_DEMANDS = 'DEMANDS'
INPUT_CHECK_FUNC = 'INPUT_CHECK_FUNC'

# core function
EXPORT_FUNC = 'EXPORT_FUNC'

# search interface: def search(keyword)
SEARCH_FUNC = 'SEARCH_FUNC'

# db interface
DATA_DIR = 'DATA_DIR'
PERSISTENCE_FUNC = 'PERSISTENCE_FUNC'
QUERY_FUNC = 'QUERY_FUNC'

BUILD_IN_VAR = [NAME,
                AUTHOR,
                DESCRIPTION,
                INPUT,
                INPUT_DEMANDS,
                EXPORT_FUNC, 
                SEARCH_FUNC,
                DATA_DIR,
                PERSISTENCE_FUNC,
                QUERY_FUNC,
                RESULT_DESC,
                INPUT_CHECK_FUNC]

########################################################################
class Mod(object):
    """"""
    
    #----------------------------------------------------------------------
    def init(self):
        """"""
        pass
    

########################################################################
class ModBase(Mod):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, name, min_threads=5, max_threads=20, debug=True,
                 loop_interval=0.2, adjuest_interval=3, diviation_ms=100):
        """Constructor"""
        Mod.__init__(self)
        
        self._name = name
        
        #
        # initial pool
        #
        self._min = min_threads
        self._max = max_threads
        self.pool = ThreadPoolX(min_threads=self._min, max_threads=self._max,
                                 name=name, debug=debug, loop_interval=loop_interval,
                                 adjuest_interval=adjuest_interval, 
                                 diviation_ms=diviation_ms )
        self.pool.start()
        
        #
        # set result recv and callback
        #
        self._result_queue = queue.Queue()
        self.pool.add_callbacks(callback=self._feed_result)
        
        self._core_func = None
        
    
    #----------------------------------------------------------------------
    def _feed_result(self, result):
        """"""
        self._result_queue.put(result)
    
    #----------------------------------------------------------------------
    def execute(self, modinput_dict):
        """"""
        assert isinstance(modinput_dict, dict)
        modinput_dict = self.check_params(modinput_dict)
        self.pool.feed(target=self._exec, vargs=(modinput_dict, ))
    
    #----------------------------------------------------------------------
    def check_params(self, params):
        """"""
        return params
    
    #----------------------------------------------------------------------
    def _exec(self, modinput_dict):
        """"""
        _r = self._core_func(**modinput_dict)
        result = {'start_time':time.time(),
                  'from':str(self._core_func),
                  'payload':modinput_dict,
                  'result':_r}
    
    @property
    def result_queue(self):
        """"""
        return self._result_queue
    
    @property
    def pool_status(self):
        """"""
        return self.pool.dumped_status()
    
    #----------------------------------------------------------------------
    def join(self):
        """"""
        self.pool.join()
    
    #----------------------------------------------------------------------
    def close(self):
        """"""
        self.pool.quit()


########################################################################
class ModBasic(ModBase):
    """"""

    #----------------------------------------------------------------------
    def from_function(self, func):
        """"""
        assert callable(func), 'func is not a callable function or method.'
        self._core_func = func
    
    #----------------------------------------------------------------------
    def from_module(self, module_obj):
        """"""
        assert hasattr(module_obj, 'EXPORT_FUNC')
        
        self._core_func = getattr(module_obj, 'EXPORT_FUNC')
        

########################################################################
class ModFunction(ModBase):
    """"""

    #----------------------------------------------------------------------
    def from_function(self, func):
        """"""
        assert callable(func), 'func is not a callable function or method.'
        self._core_func = func

########################################################################
class ModStandard(ModBase):
    """"""
    
    #----------------------------------------------------------------------
    def init(self):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def default_datadir(self, name):
        """"""
        _dir = os.path.join(_DEFAULT_DATAS_PATH, name)
        if os.path.exists(_dir):
            pass
        else:
            os.mkdir(_dir)
            
        return _dir
    
    #
    # define standard mod obj, containing description/author/demands
    #
    #----------------------------------------------------------------------
    def from_module(self, module_obj):
        """"""
        assert isinstance(module_obj, types.ModuleType)
        
        #
        # process name/author/description/data_dir
        #
        if hasattr(module_obj, NAME):
            self.NAME = getattr(module_obj, NAME)
        else:
            self.NAME = self._name
            
        if hasattr(module_obj, AUTHOR):
            self.AUTHOR = getattr(module_obj, AUTHOR)
        else:
            self.AUTHOR = 'vikit'
        
        if hasattr(module_obj, DESCRIPTION):
            self.DESCRIPTION = getattr(module_obj, DESCRIPTION)
        else:
            self.DESCRIPTION = 'No Description For module'
            
        if hasattr(module_obj, DATA_DIR):
            self.DATA_DIR = getattr(module_obj, DATA_DIR)
        else:
            self.DATA_DIR = self.default_datadir(self.NAME)
        
        #
        # process result_desc/export_func/
        #
        assert hasattr(module_obj, RESULT_DESC)
        self.RESULT_DESC = getattr(module_obj, RESULT_DESC)
        
        assert hasattr(module_obj, EXPORT_FUNC)
        assert callable(getattr(module_obj, EXPORT_FUNC))
        self._core_func = getattr(module_obj, EXPORT_FUNC)
        
        assert hasattr(module_obj, INPUT)
        self.DEMANDS = getattr(module_obj, INPUT)
        
        #
        # default callable functions: INPUT_CHECK_FUNC/SEARCH_FUNC
        #                             /PERSISTENCE_FUNC/QUERY_FUNC
        if hasattr(module_obj, INPUT_CHECK_FUNC):
            _ = getattr(module_obj, INPUT_CHECK_FUNC)
            assert callable(_)
            self.INPUT_CHECK_FUNC = _
        else:
            self.INPUT_CHECK_FUNC = self._check_input
            
        if hasattr(module_obj, SEARCH_FUNC):
            _ = getattr(module_obj, SEARCH_FUNC)
            assert callable(_)
            self.SEARCH_FUNC = _  
        else:
            self.SEARCH_FUNC = self._search_from_db
        
        if hasattr(module_obj, PERSISTENCE_FUNC):
            _ = getattr(module_obj, PERSISTENCE_FUNC)
            assert callable(_)
            self.PERSISTENCE_FUNC = _
        else:
            self.PERSISTENCE_FUNC = self._persistence_func
        
        if hasattr(module_obj, QUERY_FUNC):
            _ = getattr(module_obj, QUERY_FUNC)
            assert callable(_)
            self.QUERY_FUNC = _
        else:
            self.QUERY_FUNC = self._query_func
    
    #----------------------------------------------------------------------
    def _query_func(self, key):
        """"""
        
            
    #----------------------------------------------------------------------
    def _persistence_func(self, json_content, key=None):
        """"""
        
    
    #----------------------------------------------------------------------
    def _search_from_db(self, keywords):
        """"""
        
    
    #----------------------------------------------------------------------
    def _check_input(self):
        """"""
        assert isinstance(self.DEMANDS)
        
    
    