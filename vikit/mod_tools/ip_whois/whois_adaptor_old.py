#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<4dogs.cn>
  Purpose: whois information
  Created: 2016/10/23
"""

import unittest
import socket
from ipwhois import ipwhois

from plugin_master.plugin_manager import PluginManager
from plugin_master.plugin_base import PluginBase
from plugin_master.plugin_base import PluginParam

########################################################################
class IPWhois(PluginBase):
    """"""
    
    def config(self):
        
        self.author = 'v1ll4n'
        self.set_name('ipwhois')
        self.set_description('Retrive IP whois info')
        
        self.add_param(PluginParam(name='target', require=True,
                                   descriptions='The domain you want to check ipwhois'))
      
        
    def attack(self):
        
        options = self.get_options()
        target = options['target']
        result = ipwhois(target)
"""
{'asn': '25820',
 'asn_cidr': '45.78.0.0/19',
 'asn_country_code': 'CA',
 'asn_date': '2015-05-05',
 'asn_registry': 'arin',
 'nets': [{'address': '15216 North Bluff Road\nSuite 619',
   'cidr': '45.78.0.0/18',
   'city': 'White Rock',
   'country': 'CA',
   'created': '2015-05-05',
   'description': 'IT7 Networks Inc',
   'emails': ['abuse@sioru.com', 'arin-tech@sioru.com', 'arin-noc@sioru.com'],
   'handle': 'NET-45-78-0-0-1',
   'name': 'IT7NET',
   'postal_code': 'V4B 0A7',
   'range': '45.78.0.0 - 45.78.63.255',
   'state': 'BC',
   'updated': '2015-05-05'},
  {'address': '530 W 6th Street',
   'cidr': '45.78.0.0/19',
   'city': 'Los Angeles',
   'country': 'US',
   'created': '2015-05-06',
   'description': 'IT7 Networks Inc',
   'emails': ['abuse@sioru.com', 'arin-tech@sioru.com', 'arin-noc@sioru.com'],
   'handle': 'NET-45-78-0-0-2',
   'name': 'IT7NET-45-78-0-0-19',
   'postal_code': '90014',
   'range': None,
   'state': 'CA',
   'updated': '2015-05-06'}],
 'nir': None,
 'query': '45.78.6.64',
 'raw': None,
 'raw_referral': None,
 'referral': None}
"""

def ipwhois(domain):
    ipaddr = socket.gethostbyname(domain)
    return ipwhois.IPWhois(ipaddr).lookup_whois()

if __name__ == '__main__':
    unittest.main()