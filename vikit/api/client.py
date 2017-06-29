#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: API for client
  Created: 06/29/17
"""

from scouter.sop import FSM

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

_fsm = FSM(state_START, state_CLOSE,
           [state_CLOSE, state_CONNECTED, state_START])

#----------------------------------------------------------------------
def get_client():
    """"""
    global CLIENT
    return CLIENT

@_fsm.transfer(state_START, state_CONNECTED)
def twisted_start_client(platform_host='127.0.0.1', platform_port=7000, 
                         async=True, id=None, **config):
    """"""
    global CLIENT, CONFIG, ID
    
    ID = id if id else getuuid()
    CONFIG = twisteduserclient.ClientConfig(platform_host, platform_port,
                                            **config)
    CLIENT = twisteduserclient.TwistedClient(ID, CONFIG)
    
    CLIENT.start()
    
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
    client.

#----------------------------------------------------------------------
def execute():
    """"""
    