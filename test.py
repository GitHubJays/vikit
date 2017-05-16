#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test for vikit
  Created: 05/16/17
"""

from __future__ import unicode_literals

import unittest
from vikit.core.target import Target, TargetEnum, \
     TYPE_IPV4, TYPE_IPV6, TYPE_NETLOC, \
     TYPE_URL, TYPE_RAW, TYPE_AUTO, TYPE_FILE

from vikit.core.payload import Payload, PayloadEnum, TYPE_TEXT, TYPE_FILE
from vikit.core.mixer import mixer


########################################################################
class VikitTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_core(self):
        """"""
        #
        # test target/targets
        #
        _target = Target(target='45.78.6.64', type=TYPE_AUTO)
        self.assertEqual(_target.type, TYPE_IPV4)
        
        _targets = TargetEnum(targets=['45.78.6.64', '54.34.23.6'], type=TYPE_IPV4)
        _targets = TargetEnum(targets=['45.78.6.64:34', '54.34.23.6:76'], type=TYPE_IPV4)
        _targets = TargetEnum(targets=['tbis.me:23', 'sss.com:80'], type=TYPE_NETLOC)
        _targets = TargetEnum(targets=['http://tbis.me:23', 'http://sss.com:80'], type=TYPE_URL)
        _targets1 = TargetEnum(targets=['README.md'], type=TYPE_FILE)
        
        #
        # test payload/payloads
        #
        _pl = Payload('asdfasdf', TYPE_TEXT)
        _pl = Payload('safsadf', TYPE_TEXT)
        _pl = Payload('README.md', TYPE_TEXT)
        _pls = PayloadEnum(['README.md', 'test.py'], TYPE_TEXT)

        #
        # target/payload mix 
        #
        count = 0
        for i in mixer(_pl, _targets):
            count = count + 1
        self.assertEqual(count, 2)        
        
        count = 0
        for i in mixer(_pls, _targets):
            count = count + 1
        self.assertEqual(count, 4)



if __name__ == '__main__':
    unittest.main()