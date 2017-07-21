#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: template of plugin adaptor
  Created: 2016/11/20
"""

import unittest

from driver.plugin_driver import PluginParam
from driver.plugin_driver import PluginBase
from manager import regist

#import custom_function
import whois


########################################################################
class Whois(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """Config basic information"""
        self.name = 'whois'
        self.group = 'info_collect'
        self.description = 'Check A Domain For Whois Information'

        self.add_param(PluginParam(name='target', require=True,
                                   description='The domain you want to check'))

    #----------------------------------------------------------------------
    def attack(self):
        """"""
        # yield your result

        options = self.get_options()
        target = options['target']
        result = whois.whois(target)        
        #print 'result is ' , result
        _result = {}
        for i in result.items():
            _result[i[0]] = str(i[1])
        yield _result

regist(Whois())

if __name__ == '__main__':
    unittest.main()