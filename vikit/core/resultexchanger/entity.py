#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: 
  Created: 06/26/17
"""

import os
import pickle

from ..dbm import kvpersist

_CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

DEFAULT_DB_DIR = os.path.join(_CURRENT_PATH, '../../datas/')

########################################################################
class ResultCacher(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, bdb_filename):
        """Constructor"""
        self.bdb_filename = os.path.join(DEFAULT_DB_DIR, bdb_filename)
        self.bdb = kvpersist.KVPersister(bdb_filename)
    
    #----------------------------------------------------------------------
    def save_result(self, task_id, result_obj):
        """"""
        _ser = pickle.dumps(result_obj)
        self.bdb.set(task_id, _ser)
    
    #----------------------------------------------------------------------
    def load_result(self, task_id):
        """"""
        _ser = self.bdb.get(task_id)
        if _ser:
            return pickle.loads(_ser)
        else:
            return None
    
    #----------------------------------------------------------------------
    def delete_result(self, task_id):
        """"""
        self.bdb.delete(task_id)


########################################################################
class TaskIdCacher(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, cache_task_id_filename):
        """Constructor"""
        self.cache_task_id_filename = os.path.join(DEFAULT_DB_DIR, cache_task_id_filename)
        self._list_task_ids = None
        
        _text = None
        if not os.path.exists(self.cache_task_id_filename):
            fp = open(self.cache_task_id_filename, 'wb')
            fp.write('')
            fp.close()
        else:
            pass
        with open(self.cache_task_id_filename, 'rb') as f:
            _text = f.read()
        
        if _text:
            try:
                self._list_task_ids = pickle.loads(_text)
            except:
                self._list_task_ids = []
        else:
            self._list_task_ids = []
            
    #----------------------------------------------------------------------
    def push_one(self, task_id):
        """"""
        if task_id in self._list_task_ids:
            pass
        else:
            self._list_task_ids.append(task_id)
            
    #----------------------------------------------------------------------
    def peek_one(self, index=0):
        """"""
        if len(self._list_task_ids) > 0:
            try:
                _id = self._list_task_ids[index]
            except:
                _id = None
        else:
            _id = None
            
        return _id
    
    #----------------------------------------------------------------------
    def remove_one(self, task_id):
        """"""
        try:
            self._list_task_ids.remove(task_id)
        except:
            pass
    
    #----------------------------------------------------------------------
    def save(self):
        """"""
        try:
            _text = pickle.dumps(self._list_task_ids)
        except:
            _text = pickle.dumps([])
            
        with open(self.cache_task_id_filename, 'wb') as fp:
            fp.write(_text)


        
    
    
    