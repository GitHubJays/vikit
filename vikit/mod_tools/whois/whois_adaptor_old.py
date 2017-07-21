#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<4dogs.cn>
  Purpose: whois information
  Created: 2016/10/23
"""

import unittest
import socket
import whois

from plugin_master.plugin_manager import PluginManager
from plugin_master.plugin_base import PluginBase
from plugin_master.plugin_base import PluginParam

########################################################################
class Whois(PluginBase):
    """"""

    def config(self):

        self.author = 'v1ll4n'
        self.set_name('whois')
        self.set_description('Retrive domain whois info')

        self.add_param(PluginParam(name='target', require=True,
                                   descriptions='The domain you want to check'))


    def attack(self):

        options = self.get_options()
        target = options['target']
        result = dwhois(target)
        return result


def dwhois(domain):
    return whois.whois(domain)

if __name__ == '__main__':
    unittest.main()