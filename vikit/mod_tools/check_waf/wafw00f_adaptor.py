#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<4dogs.cn>
  Purpose: check waf
  Created: 2016/10/24
"""

from plugin_master.plugin_manager import PluginManager
from plugin_master.plugin_base import PluginBase
from plugin_master.plugin_base import PluginParam
from plugin_master.plugin_manager import plugin_regist

import unittest

from check_waf import checkWaf

########################################################################
class CheckWaf(PluginBase):
    """
    Check WAF
    """
    def config(self):
        self.set_name('check_waf')
        self.set_group('info_collect')
        self.set_description('Check the waf existed')
        
        self.add_param(PluginParam(name='target', require=True, 
                                   descriptions='The target you want to check waf'))

    def attack(self):
        target = self.get_options()['target']
        return checkWaf(target).run()
    
        
    
plugin_regist(CheckWaf())    
    

if __name__ == '__main__':
    unittest.main()