#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: User Client For Service
  Created: 06/07/17
"""

from twisted.internet.protocol import ClientFactory

from ..basic import serializer
from ..common import baseprotocol
from ..common import welcome
from .client_entity import VikitClient
from ..common import userclientop
from ..utils import getuuid

########################################################################
class ServiceClientForUser(baseprotocol.VikitProtocol):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, id, client_ins, cryptor=None, *v, **kw):
        """Constructor"""
        self._cryptor = cryptor
        baseprotocol.VikitProtocol.__init__(self, *v, **kw)

        #
        # id
        #
        self._id = id

        #
        # bind client
        #
        assert isinstance(client_ins, VikitClient)
        self.client = client_ins

        #
        # set flags
        #
        self._working_flag = False

    #----------------------------------------------------------------------
    def init_cryptor(self):
        """"""
        assert isinstance(self.serializer, serializer.Serializer)
        self.serializer.set_cryptor(self._cryptor)

    @property
    def id(self):
        """"""
        return self._id

    #----------------------------------------------------------------------
    def connectionMade(self):
        """"""
        self.send(welcome.WelcomeBase(self.id))


    #----------------------------------------------------------------------
    def handle_obj(self, obj):
        """"""
        if not self._working_flag:
            if isinstance(obj, welcome.WelcomeBase):
                self.client.add_service(id, self)
        else:
            if isinstance(obj, userclientop.VikitResultInProto):
                self.client.finish_task(obj)



########################################################################
class ServiceClientForUserFactory(ClientFactory):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, client_ins, cryptor):
        """Constructor"""
        self._client_instance = client_ins
        self._cryptor = cryptor
    
    #----------------------------------------------------------------------
    def buildProtocol(self):
        """"""
        return ServiceClientForUser(getuuid(), self._client_instance, self._cryptor)
        
        
    
    