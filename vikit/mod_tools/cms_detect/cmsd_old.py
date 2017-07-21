#encoding:utf-8

#


#def run(url):
    #result = app_detect(url)
    
    ##Control result output
    #return result


#if __name__ == '__main__':
    #print run(url='https://blog.tbis.me')

#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<4dogs.cn>
  Purpose: 
  Created: 2016/10/23
"""

import unittest

from plugin_master.plugin_manager import PluginManager
from plugin_master.plugin_base import PluginBase
from plugin_master.plugin_base import PluginParam



from cms_detect.WapBanner import app_detect
########################################################################
class CMSDetect(PluginBase):
    """
    Detect CMS type and other webapp information
    """
    
    def config(self):
        self.set_name('cms_detect')
        self.add_param(PluginParam(name='target', require=True))
        self.author = '4dogs.cn'
        self.set_description('Detect CMS type and the server type')
        
    def attack(self):
        return app_detect(self.get_param_value('target'))
        
    
if __name__ == '__main__':
    unittest.main()