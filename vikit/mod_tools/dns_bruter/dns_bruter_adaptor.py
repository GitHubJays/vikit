#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: dns bruter pro
  Created: 2016/11/20
"""

import unittest

from driver.plugin_driver import PluginParam
from driver.plugin_driver import PluginBase
from manager import regist
from types import NoneType

from bruter import DNSBruter
#import custom_function

########################################################################
class DNSBruterAdaptor(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """Config basic information"""
        self.name = 'dns_bruter'
        self.group = 'info_collect'
        self.author = 'v1ll4n'
        self.description = 'guess DNS subdomain'

        self.add_param(PluginParam(name='target', require=True,
                                   description='the base domain you want to guess'))
        self.add_param(PluginParam(name='thread_max', type=int, default=30,
                                   description='the max thread for ThreadPool'))
        self.add_param(PluginParam(name='nameserver', type=list, default=[],
                                   description='Constom Nameservers'))
        self.add_param(PluginParam(name='dict_file', default=None, type=NoneType, require=False,
                                   description='dict_file path'))
        self.add_param(PluginParam(name='do_continue', type=bool, default=True,
                                   description='Do you want to continue the work?'))
        self.add_param(PluginParam(name='session_id', default='dns_bruter_session',
                                   description='set session for continue'))
        self.add_param(PluginParam(name='timeout', type=int, default=5,
                                   description='timeout for each query'))
        self.add_param(PluginParam(name='clean_mod', type=bool, default=True,
                                   description='clean mod for threadpool?'))

    #----------------------------------------------------------------------
    def attack(self):
        """"""
        # yield your result
        options = self.get_options()
        
        bruteri = DNSBruter(**options)
        result_queue = bruteri.start()
        while True:
            ret = result_queue.get()
            if ret.get('state'):
                yield ret.get('result')
        
regist(DNSBruterAdaptor())

if __name__ == '__main__':
    unittest.main()