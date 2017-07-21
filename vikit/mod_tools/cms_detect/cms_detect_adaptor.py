#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Detected WEB APP TYPE
  Created: 2016/11/21
"""

import unittest

from driver.plugin_driver import PluginBase
from driver.plugin_driver import PluginParam
from manager import regist


from cms_detect.WapBanner import app_detect

########################################################################
class CMSDetect(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """"""
        self.name = 'cms_detect'
        self.description = 'Detect Type of Web App, Not only CMS'
        self.group = 'info_collect'
        
        self.add_param(PluginParam(name='target', 
                                   description='The website you want to check',
                                   require=True))
        
    #----------------------------------------------------------------------
    def attack(self):
        """"""
        yield app_detect(self.get_param('target').get_value())
        
regist(CMSDetect())
    

if __name__ == '__main__':
    unittest.main()