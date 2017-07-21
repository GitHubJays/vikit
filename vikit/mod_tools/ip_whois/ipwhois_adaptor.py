#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: IPWHOIS
  Created: 2016/11/21
"""

import unittest
from ipwhois import ipwhois

from driver.plugin_driver import PluginBase
from driver.plugin_driver import PluginParam
from manager import regist

########################################################################
class IPWhois(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """"""
        self.name = 'ip_whois'
        self.description = 'Check the information of IP Addr'
        self.group = 'info_collect'
        
        self.add_param(PluginParam(name='target', 
                                   description='The IP you want to check',
                                   require=True))
        
    #----------------------------------------------------------------------
    def attack(self):
        """"""
        ipw = ipwhois.IPWhois(self.get_param('target').get_value())
        try:
            yield ipw.lookup()
        except:
            pass
        
        try:
            yield ipw.lookup_rdap()
        except:
            pass
        
        try:
            yield ipw.lookup_whois()
        except:
            pass
        
        try:
            yield {'dns_zone':ipw.dns_zone}
        except:
            pass
        
regist(IPWhois())
    

if __name__ == '__main__':
    unittest.main()