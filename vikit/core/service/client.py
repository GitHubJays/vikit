#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client For Service
  Created: 05/22/17
"""

import uuid

from twisted.internet.protocol import Protocol, ClientFactory
from twisted.internet import reactor

from . import actions

TASK_STATE_FINISHED = 'finished'
TASK_STATE_TIMEOUT = 'timeout'
TASK_STATE_PENDING = 'pending'
TASK_STATE_NOT_EXISTED = 'not_exsted'
TASK_STATE_ERROR = 'error'

#
# client for service
#
########################################################################
class VClient(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, rhost, rport, crypto=None):
        """Constructor"""
        #
        # client id (Client+uuid)
        #
        self._cid = 'Client-' + uuid.uui1().hex
        
        #
        # service port
        #
        self._rhost = rhost
        self._rport = rport
        
        #
        # enc mod
        #
        self._cryptor = crypto
        
        #
        # task state
        #
        self._task_status = {}
    
    @property
    def cid(self):
        """"""
        return self._cid
    
    @property
    def conn(self):
        """"""
        if self._conn:
            return self._conn
        else:
            return None
    
    #----------------------------------------------------------------------
    def connect(self, rhost, rport, crypto):
        """"""
        
    #
    # bind conn to client
    #
    #----------------------------------------------------------------------
    def add_bind(self, conn):
        """"""
        assert isinstance(conn, Protocol)
        self._conn = conn
    
    #----------------------------------------------------------------------
    def execute(self, params):
        """"""
        self._check_conn()
        #assert isinstance(self.conn, Protocol), 'bind connection before execute!'
        
        #
        # send to remote service
        #
        tid = self._gen_task_id()
        cid = self.cid
        assert isinstance(params, dict)
        
        task = actions.Task(cid, task_id, params)
        
        self.conn.send(task)
    
    #----------------------------------------------------------------------
    def _check_conn(self):
        """"""
        assert isinstance(self.conn, Protocol), 'bind connection before execute!'
        
        
    #----------------------------------------------------------------------
    def query_task_status(self, task_id):
        """"""
        self._check_conn()
        
        query = actions.QueryTaskStatus(self.cid, task_id)
        self.conn.send(query)
    
    #----------------------------------------------------------------------
    def update_task_status(self, task_obj):
        """"""
        self._check_conn()
        
        assert isinstance(task_obj, actions.TaskStatus)
        
        
    
    #----------------------------------------------------------------------
    def proccess_result(self, result):
        """"""
        #
        # 
        #
    
    #----------------------------------------------------------------------
    def dump_status(self):
        """"""
        return self._task_status

    #----------------------------------------------------------------------
    def _gen_task_id(self):
        """"""
        return uuid.uuid1().hex
        
        
        
    
    