#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Service
  Created: 06/05/17
"""

from ..common import baseprotocol, welcome, serviceop
from .vikitservice_entity import VikitService

########################################################################
class VikitServiceConn(baseprotocol.VikitProtocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_ins, *v, **kw):
        """Constructor"""
        self.service = service_ins
        assert isinstance(self.service, VikitService)
        self.cryptor = self.service.config.cryptor
        baseprotocol.VikitProtocol.__init__(self, *v, **kw)
        
        self._registed = False
        
        self.id = None
    
    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        self.serializer.set_cryptor(self.cryptor)
        
    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        if not self._registed:
            if isinstance(obj, welcome.UserWelcome):
                self.id = obj.id
                self.service.handle_welcome(obj.id, self)
        else:
            if isinstance(obj, serviceop.VikitTaskInProto):
                obj.client_id = self.id
                self.service.handle_task(obj)
    
    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        self.send(welcome.WelcomeBase(self.id))
        
        
    
    