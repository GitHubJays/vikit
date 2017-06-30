#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: API for client
  Created: 06/29/17
"""

from scouter.sop import FSM
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from ..apps import twisteduserclient
from ..core.utils import getuuid

CLIENT = None
CONFIG = twisteduserclient.ClientConfig()
ID = None

#
# define fsm
#
state_START = 'start'
state_CONNECTED = 'connected'
state_CLOSE = 'close'

action_START_SUCCESS = 'start_success'
action_START_ERROR = 'start_error'
action_SHUTDOWN = 'shutdown'

_fsm = FSM(state_START, state_CLOSE,
           [state_CLOSE, state_CONNECTED, state_START])

_fsm.create_action(action_START_SUCCESS, state_START, state_CONNECTED)
_fsm.create_action(action_START_ERROR, state_START, state_CLOSE)
_fsm.create_action(action_SHUTDOWN, state_CONNECTED, state_CLOSE)

#----------------------------------------------------------------------
def get_client():
    """"""
    global CLIENT
    return CLIENT

def twisted_start_client(platform_host='127.0.0.1', platform_port=7000, 
                         async=True, id=None, **config):
    """"""
    global CLIENT, CONFIG, ID
    
    ID = id if id else getuuid()
    CONFIG = twisteduserclient.ClientConfig(platform_host, platform_port,
                                            **config)
    CLIENT = twisteduserclient.TwistedClient(ID, CONFIG)
    
    CLIENT.start()
    
    __start_update_client_state_until_client_working()
    
    if not async:
        CLIENT.mainloop_start()
    else:
        pass

#----------------------------------------------------------------------
def twisted_stop_client():
    """"""
    global CLIENT
    
    CLIENT.mainloop_stop()

#----------------------------------------------------------------------
def mainloop_start():
    """"""
    client = get_client()
    assert isinstance(client, twisteduserclient.TwistedClient)
    client.mainloop_start()
    
@_fsm.onstate(state_CONNECTED)
def shutdown():
    """"""
    client = get_client()
    assert isinstance(client, twisteduserclient.TwistedClient)
    
    client.shutdown()

@_fsm.onstate(state_CONNECTED)
def execute(module_name, params, offline=False, task_id=None, callback_chains=[]):
    """"""
    task_id = task_id if task_id else getuuid()
    
    client = get_client()
    
    try:
        client.execute(module_name, params, offline, task_id, callback_chains)
    except twisteduserclient.ClientError:
        task_id = None
    
    return task_id

@_fsm.onstate(state_CONNECTED)
def get_available_modules():
    """list for available services module"""
    return get_client().get_available_modules()

@_fsm.onstate(state_CONNECTED)
def get_help_for_module(module_name):
    """dict for help info service module"""
    return get_client().get_help_for_module(module_name)

#----------------------------------------------------------------------
def can_execute_tasks():
    """"""
    client = get_client()
    if client.state == twisteduserclient.state_WORKING:
        return True
    else:
        return False

#----------------------------------------------------------------------
def __start_update_client_state_until_client_working():
    """"""
    global _fsm
    client = get_client()
    
    def _update_client_state_until_client_working():
        print(client.state)
        if client.state == twisteduserclient.state_WORKING:
            _fsm.action(action_START_SUCCESS)
            if _loopingcall.running:
                _loopingcall.stop()
        else:
            pass
    
    _loopingcall = LoopingCall(_update_client_state_until_client_working)
    _loopingcall.start(0.3)
    