#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Det C Class IP addr Alive
  Created: 2016/12/26
"""

import unittest

from driver.plugin_driver import PluginParam
from driver.plugin_driver import PluginBase
from manager import regist

from isalive import is_alive
from IPy import IP
from g3ar import ThreadPool

########################################################################
class IPBlockAlive(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """Config basic information"""
        self.name = 'c_class_ip_alive'
        self.group = ['info_collect']
        self.description = 'Detect if the ip\' s C class peers are alive.'

        self.add_param(PluginParam(name='target', require=True,
                                   description='The target ip you want to check its c '+ \
                                   'block'))
        self.add_param(PluginParam(name='timeout', require=True, type=int,
                                   description='Timeout for Every Request.',
                                   default=2))
        self.add_param(PluginParam(name='count', require=True, default=4, type=int,
                                   description='The times you want to try.'))
        self.add_param(PluginParam(name='async', require=True,
                                   default=True, type=bool,
                                   description='Get Result One by One(async==True),'+\
                                   '\n Or get all at once(async==False).'))

    #----------------------------------------------------------------------
    def attack(self):
        """"""
        # yield your result
        options = self.get_options()
        
        pool = ThreadPool()
        pool.start()
        
        for i in IP(options['target']).make_net('255.255.255.0'):
            pool.feed(is_alive, i.strNormal(), options['timeout'], options['count'])  

        if options['async']:
            for j in pool.get_result_generator():
                yield j['result']
        else:
            result = {}
            for j in pool.get_result_generator():
                result = dict(result, **j['result'])
            yield result            

regist(IPBlockAlive())

if __name__ == '__main__':
    unittest.main()