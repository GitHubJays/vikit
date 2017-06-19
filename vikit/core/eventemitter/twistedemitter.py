#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Twisted Emitter
  Created: 06/17/17
"""

from twisted.internet import task

from . import emitterbase
from ..platform import vikitplatform
from ..servicenode import vikitservicenode
from ..launch.twistedlaunch import TwistdLauncher
from ..launch import twistedbase
from ..actions import servicenode_actions, heartbeat_action

########################################################################
class TwistedPlatformEventEmitter(emitterbase.EmitterBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, launcher):
        """Constructor"""
        emitterbase.EmitterBase.__init__(self, launcher)
        
        self.platform = self.launcher.entity
        assert isinstance(self.platform, vikitplatform.VikitPlatform)
        
    #----------------------------------------------------------------------
    def start_service(self, service_node_id, service_id,
                      module_name, launcher_config):
        """"""
        assert self.launcher.entity.has_service_node(service_node_id)
        
        #
        # build action
        #
        _start_service_action = servicenode_actions.StartServiceAction(service_id=service_id,
                                                                       module_name=module_name,
                                                                       launcher_type=TwistdLauncher,
                                                                       launcher_config=launcher_config)
        
        #
        # get conn
        #
        _record = self.platform.get_service_node_record(service_node_id)
        _conn = _record.get('twisted_conn')
        assert isinstance(_conn, twistedbase.VikitTwistedProtocol)
        
        #
        # send it
        #
        _conn.send(_start_service_action)
    
    #----------------------------------------------------------------------
    def get_service_info(self):
        """"""
        return self.platform.get_service_info()

########################################################################
class TwistedServiceNodeEventEmitter(emitterbase.EmitterBase):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, connector):
        """Constructor"""
        emitterbase.EmitterBase.__init__(self, connector)
        
        self.servicenode = connector.entity
        assert isinstance(self.servicenode, vikitservicenode.VikitServiceNode) 
        
        self._loopingcall_heartbeat = task.LoopingCall(self._send_heartbeat)
    
    #----------------------------------------------------------------------
    def get_sender(self):
        """"""
        return self.launcher.connector.transport.protocol
        
    
    #----------------------------------------------------------------------
    def regist_start_heartbeat_callback(self):
        """"""
        self.servicenode.regist_start_heartbeat_callback(self._start_heartbeat)
        #return 
    
    #----------------------------------------------------------------------
    def _start_heartbeat(self, interval):
        """"""
        if self._loopingcall_heartbeat.running:
            self._loopingcall_heartbeat.stop()
            self._loopingcall_heartbeat.start(interval, True)
        else:
            self._loopingcall_heartbeat.start(interval, True)
    
    #----------------------------------------------------------------------
    def _send_heartbeat(self):
        """"""
        _heartbeat = self.servicenode.get_heartbeat_obj()
        _connector = self.get_sender()
        #print(_connector)
        assert isinstance(_connector, twistedbase.VikitTwistedProtocol)
        print(_heartbeat)
        _connector.send(_heartbeat)