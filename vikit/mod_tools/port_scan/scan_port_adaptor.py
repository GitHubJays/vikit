#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Scan Port
  Created: 2016/12/19
"""

import unittest

from driver.plugin_driver import PluginParam
from driver.plugin_driver import PluginBase
from manager import regist

from scan_port import QuickPortScanner
from nmaplib import nmap_options
#import custom_function

########################################################################
class QuickerPortScannerAdaptor(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """Config basic information"""
        self.name = 'port_scan'
        self.group = 'info_collect'
        self.description = 'Scan Port Based-on nmap'

        self.add_param(PluginParam(name='target', require=True,
                                   description='The target host you want to scan'))
        self.add_param(PluginParam(name='ports', require=False, default='',
                                   description='The ports you want to scan' + \
                                   '\n default port is [common ports by nmap]',
                                   type=str))
        self.add_param(PluginParam(name='extra_arg', require=False, default='',
                                   description='More Extra arg for nmap'))
        self.add_param(PluginParam(name='default_arguments', require=False, 
                                   default=nmap_options.DEFAULT_ARUGUMENTS_WITH_VERSION_DETECTION_PRO))
        self.add_param(PluginParam(name='timeout', require=True, type=(int, float),
                                   description='Timeout for every request',
                                   default=10))
        self.add_param(PluginParam(name='max_pool_threads', default=30, require=True,
                                   description='Max Threads amount!', 
                                   type=int))

    #----------------------------------------------------------------------
    def attack(self):
        """"""
        options = self.get_options()
        # yield your result
        quick_port_scanner = QuickPortScanner(**options)
        result_queue = quick_port_scanner.start()
        for i in xrange(quick_port_scanner.task_count):
            try:
                yield result_queue.get().get('result')
            except:
                yield result_queue.get()
regist(QuickerPortScannerAdaptor())

if __name__ == '__main__':
    unittest.main()