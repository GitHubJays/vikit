#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: DNS digger
  Created: 2016/12/1
"""

from pprint import pprint
import unittest

from dns_dig_lib import dns_query_all
from dns_dig_lib import dns_zone_transfer_check
from dns_dig_lib import dns_query_quick



########################################################################
class DNSDigger(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, target, quick_mode=True):
        """Constructor"""
        assert isinstance(target, (str, unicode))
        
        self.target = target
        self.result = {}
        
        self._quick_mode = quick_mode 
    #----------------------------------------------------------------------
    def get_result(self):
        """"""
        if self._quick_mode == False:
            self.query_result = dns_query_all(self.target)
        else:
            self.query_result = dns_query_quick(self.target)
        self.ns_servers = self.get_ns_servers()
        zonet = self.get_dns_zone_transfer_result()
        
        self.result['query'] = self.query_result
        self.result['zone_transfer'] = zonet
        return self.result 

    #----------------------------------------------------------------------
    def get_ns_servers(self):
        """"""
        _ns_server_raws = []
        try:
            _ = self.query_result['NS']
        except AttributeError:
            return []
        
        for i in _:
            _ns_server_raws.append(i.split()[-1])
        
        return _ns_server_raws
    
    #----------------------------------------------------------------------
    def get_dns_zone_transfer_result(self):
        """"""
        result = {}
        result['zone_transfer'] = False
        result['result'] = ''
        
        for i in self.ns_servers:
            ret = dns_zone_transfer_check(self.target, i)
            if ret == "":
                pass
            else:
                result['result'] = result['result'] + ret + '\n'
        
        if result['result'] != '':
            result['zone_transfer'] = True
            
        return result
                

########################################################################
class DNSDigTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        #ret = DNSDigger('sdp.edu.cn')
        ret = DNSDigger('henu.edu.cn')
        pprint(ret.get_result())
    
if __name__ == '__main__':
    unittest.main()