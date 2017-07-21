#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Brute Path Plugin
  Created: 2016/11/20
"""

import unittest

from driver.plugin_driver import PluginParam
from driver.plugin_driver import PluginBase
from manager import regist

from brute_path import BrutePath

########################################################################
class BrutePathAdaptor(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """Config basic information"""
        self.name = 'brute_path'
        self.group = 'info_collect'
        self.description = 'Force Bruting Web Path'

        self.add_param(PluginParam(name='target', require=True,
                                   description='The URL you want to force bruting.'))
        self.add_param(PluginParam(name='headers', require=False, default={},
                                   description='The HTTP headers(INPUT JSON DATA)',
                                   type=dict))
        self.add_param(PluginParam(name='cookie', require=False, default={},
                                   description='The Cookie you want to use',
                                   type=(dict, str,)))
        self.add_param(PluginParam(name='dict_file', require=True, default='dicts/dir.txt',
                                   description='The Dict you want to use',))
        self.add_param(PluginParam(name='timeout', require=True, default=5, 
                                   description='timeout for requesting a single page',
                                   type=int))
        self.add_param(PluginParam(name='max_pool_threads', require=True,
                                   default=30,
                                   description='max threads of thread pool',
                                   type=int))
        self.add_param(PluginParam(name='session_id', require=True, default='default',
                                   type=str, description='remember the Session ID to continue\
                                   your progress'))
        self.add_param(PluginParam(name='do_continue', require=True, default=False,
                                   description='Continue or not(session_id shuold be define)',
                                   type=bool))

    #----------------------------------------------------------------------
    def attack(self):
        """"""
        # yield your result
        options = self.get_options()
        bruter = BrutePath(**options)
        queue = bruter.start()
        while bruter.finished == False:
            #print 'GETTING RESULT'
            ret = queue.get()
            #print ret
            yield ret

regist(BrutePathAdaptor())

if __name__ == '__main__':
    unittest.main()