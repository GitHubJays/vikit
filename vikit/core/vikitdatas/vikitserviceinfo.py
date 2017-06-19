#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Service Info
  Created: 06/17/17
"""

from . import base
from . import vikitservicedesc
from . import vikitservicelauncherinfo

########################################################################
class VikitServiceInfo(base.VikitDatas):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, service_node_id, desc, launcherinfo):
        """Constructor"""
        assert isinstance(desc, vikitservicedesc.VikitServiceDesc)
        assert isinstance(launcherinfo, vikitservicelauncherinfo.VikitServiceLauncherInfo)
        
        self.desc = desc
        self.linfo = launcherinfo
        self.service_node_id = service_node_id
    
    #----------------------------------------------------------------------
    def get_dict(self):
        """"""
        return {'desc':self.desc.get_dict(),
                'laucher_info':self.linfo.get_dict(),
                'service_node_id':self.service_node_id}
    
    @property
    def id(self):
        """"""
        return self.desc.id
        
    
    