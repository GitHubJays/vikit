#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Client Trigger
  Created: 07/02/17
"""

import sys
import os
import signal

from multiprocessing import Pipe, Process
from twisted.internet import reactor

from .. import client
from . import _base

action_get_help_for = 'get_help_for'
action_get_modules = 'get_modules'
action_execute = 'execute'
action_state = 'state'
action_shutdown = 'shutdown'


    
#----------------------------------------------------------------------
def get_client_proxy(platform_host, platform_port, id=None, **config):
    """"""
    p1, p2 = Pipe()
    
    trigger = ClientTrigger(p2, platform_host, platform_port, id, **config)
    
    #
    # prepare process and set daemon
    #
    trigger_process = Process(target=trigger.start)
    trigger_process.daemon = True
    trigger_process.start()
    
    return ClientProxy(p1, trigger_process)
    

########################################################################
class ClientProxy(_base.ProxyBase):
    """"""

    #---------------------------------------------------------------------
    def __init__(self, pipe, process):
        """Constructor"""
        
        self._pipe = pipe
        self._process = process
        
        
    #----------------------------------------------------------------------
    def _send(self, data):
        """"""
        self._pipe.send(data)
    
    #----------------------------------------------------------------------
    def execute(self, module_name, params, offline=False, task_id=None):
        """"""
        func = action_execute
        _params = {'module_name':module_name,
                  'params':params,
                  'offline':offline,
                  'task_id':task_id}
        
        data = (func, _params)
        
        self._send(data)
        
        return self._receive_data()
        
    #----------------------------------------------------------------------
    def get_available_modules(self):
        """"""
        func = action_get_modules
        params = {}
        
        data = (func, params)
        
        self._send(data)
        
        return self._receive_data()
        
    #----------------------------------------------------------------------
    def get_help_for_module(self, module_name):
        """"""
        func = action_get_help_for
        params = {'module_name':module_name}
        
        data = (func, params)
        
        self._send(data)
        
        return self._receive_data()
    
    #----------------------------------------------------------------------
    def shutdown(self):
        """"""
        func = action_shutdown
        params = {}
        
        data = (func, params)
        
        self._send(data)
        
        _ret = self._receive_data()

        try:
            pid = self._process.pid
            os.kill(pid, signal.SIGKILL)
        except:
            pass
            
        return _ret
    
    @property
    def state(self):
        """"""
        func = action_state
        params = {}
        
        data = (func, params)
        
        self._send(data)
        
        return self._receive_data()
        
    #----------------------------------------------------------------------
    def _receive_data(self):
        """"""
        while True:
            if self._pipe.poll():
                return self._pipe.recv()


########################################################################
class ClientTrigger(_base.Trigger):
    """"""

    #---------------------------------------------------------------------
    def __init__(self, pipe, platform_host, platform_port, 
                 id=None, **config):
        """Constructor"""
        self.platform_host = platform_host
        self.platform_port = platform_port
        self.id = id
        self.config = config
        
        self._pipe = pipe
    
    #----------------------------------------------------------------------
    def _recieving(self):
        """"""
        while True:
            if self._pipe.poll():
                data = self._pipe.recv()
                self._pipe.send(self.on_data_received(data))
    
    #----------------------------------------------------------------------
    def on_data_received(self, data):
        """"""
        func = data[0]
        params = data[1]
        if func == action_execute:
            return client.execute(**params)
        elif func == action_get_help_for:
            return client.get_help_for_module(**params)
        elif func == action_get_modules:
            return client.get_available_modules()
        elif func == action_state:
            return client.get_state()
        elif func == action_shutdown:
            try:
                return None #client.shutdown()
            except:
                return None
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        client.twisted_start_client(self.platform_host,
                                    self.platform_port,
                                    async=True,
                                    id=self.id,
                                    update_client_state=True,
                                    **self.config)
        
        #
        # prepare receiving data
        #
        client.call_in_thread(self._recieving)
        
        client.mainloop_start()
        
        