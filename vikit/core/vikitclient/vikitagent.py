#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Vikit Agent
  Created: 06/20/17
"""

import random

from . import vikitclient
from ..launch.twistedlaunch import TwistdConnector
from ..eventemitter import twistedemitter
from ..utils import getuuid

########################################################################
class VikitAgent(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, module_name, 
                 ack_timeout=10, retry_times=5, cryptor=None,
                 connection_timeout=30):
        """Constructor"""
        self.module_name = module_name
        
        #
        # basic attrs
        #
        self.ack_timeout = ack_timeout
        self.retry_times = retry_times
        self.cryptor = cryptor
        self.connection_timeout = connection_timeout
        
        #
        # private recording
        # 
        self._dict_client_record = {}
        self._list_result_callback = []
    
    #----------------------------------------------------------------------
    def add_service_addr(self, id, host, port):
        """"""
        #
        # client info 
        #
        _client_id = id
        _addr = (host, port)

        #
        # regist in dict_client_record
        #
        if not self._dict_client_record.has_key(_client_id):
            self._dict_client_record[_client_id] = {}
        self._dict_client_record[_client_id]['addr'] = _addr
        
        #
        # start it (fill emitter key)
        #
        _emitter = self._start_client(_client_id, _addr)
    
    #----------------------------------------------------------------------
    def _start_client(self, id, addr):
        """"""
        _client = vikitclient.VikitClient(id)
        
        #
        # regist callback
        #
        for i in self._list_result_callback:
            _client.regist_result_callback(*i)
        
        _conn = TwistdConnector(_client)
        _conn.connect(*addr, cryptor=self.cryptor,
                      ack_timeout=self.ack_timeout, retry_times=5,
                      connect_timeout=self.connection_timeout)
        
        emitter = twistedemitter.TwistedClientEventEmitter(_conn)
        self._dict_client_record[id]['emitter'] = emitter
        
        return emitter
        
        
    
    #----------------------------------------------------------------------
    def execute(self, task_id, params):
        """"""
        _client_id = self.select_service()
        if _client_id:
            emitter = self._dict_client_record.get(_client_id).get('emitter')
            assert isinstance(emitter, twistedemitter.TwistedClientEventEmitter)
            emitter.execute(task_id, params)
            
        else:
            return False
    
    #----------------------------------------------------------------------
    def select_service(self):
        """"""
        _keys = self._dict_client_record.keys()
        if _keys:
            return random.choice(_keys)
        else:
            return None
    
    #----------------------------------------------------------------------
    def regist_result_callback(self, callback, callback_excp=None):
        """"""
        if callback_excp:
            assert callable(callback_excp)
        
        assert callable(callback)
        
        self._list_result_callback.append((callback, callback_excp))
    
    
    
            
        
        
        
        
        
    
    