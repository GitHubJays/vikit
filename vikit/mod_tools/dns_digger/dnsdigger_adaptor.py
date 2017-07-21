#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: DIG INFORMATION ABOUT DNS
  Created: 2016/11/20
"""

import unittest

from driver.plugin_driver import PluginParam
from driver.plugin_driver import PluginBase
from manager import regist
from utils import clean_params_dict
from dns_dig import DNSDigger
#import custom_function

########################################################################
class NDSDiggerAdaptor(PluginBase):
    """"""

    #----------------------------------------------------------------------
    def config(self):
        """Config basic information"""
        self.name = 'dns_digger'
        self.group = 'info_collect'
        self.description = 'Find DNS information and check the zone\n \
          transfer vuln! And the zone_transfer Vuln will be check.'

        self.add_param(PluginParam(name='target', require=True,
                                   description='The domain you want to check'))
        self.add_param(PluginParam(name='quick_mode', require=True, value=True,
                                   description='If True, just query the \n\
                                   A AAAA NS MX SOA TXT CNAME, False for all!',
                                   type=bool))

    #----------------------------------------------------------------------
    def attack(self):
        """"""
        # yield your result
        options = self.get_options()
        params = clean_params_dict.dict_cleaner(options)
        digger = DNSDigger(**params)
        try:
            yield digger.get_result()
        except:
            yield {'state':False, 'result':'Something Wrong in Digger, Sorry!'}

regist(NDSDiggerAdaptor())

if __name__ == '__main__':
    unittest.main()