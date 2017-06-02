#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Platform Entity
  Created: 06/02/17
"""

from scouter.sop import FSM


from ..utils.singleton import Singleton
from ..utils import getuuid

#
# define state and FSM
#
state_START = 'start'
state_END = 'end'
state_WAITING = 'waiting'
state_RUNNING = 'running'
state_ERROR = 'error'

PFSM = FSM(state_START, state_END, 
           [state_END,
            state_ERROR,
            state_RUNNING,
            state_START,
            state_WAITING])

DEFAULT_PORT = 7000

########################################################################
class Platform(Singleton):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id=None, port=7000, net_if=''):
        """Constructor"""
        self._id = id if id else getuuid()
        self._port = port if port else DEFAULT_PORT
        self._nif = net_if if net_if else ''
    
    
    
    