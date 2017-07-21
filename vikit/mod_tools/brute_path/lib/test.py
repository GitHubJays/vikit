#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test basic lib for brute path
  Created: 2016/12/14
"""

import unittest

from connect import request_page 
from requests import Response


########################################################################
class BruteTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_single_request(self):
        """Constructor"""
        rsp = request_page(url, headers={}, cookies={})
        self.assertIsInstance(rsp, Response)
        
        
    
    

if __name__ == '__main__':
    unittest.main()