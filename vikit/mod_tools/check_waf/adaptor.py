#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: check waf
  Created: 2016/11/20
"""

import unittest

from driver.plugin_driver import PluginParam
from driver.plugin_driver import PluginBase
from manager import regist

from check_waf import checkWaf

########################################################################
class CheckWaf(PluginBase):
    """"""
    
    #----------------------------------------------------------------------
    def config(self):
        """Config basic information"""
        self.name = 'check_waf'
        self.group = 'info_collect'
        self.description = 'Check Waf for a website'
        
        self.add_param(PluginParam(name='target', require=True,
                                   description='The url you want check'))

    #----------------------------------------------------------------------
    def attack(self):
        """"""
        target = self.get_param('target').get_value()
        
        yield checkWaf(target).run()

regist(CheckWaf())

if __name__ == '__main__':
    unittest.main()