#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test Workflow
  Created: 06/26/17
"""

import unittest

from vikit.core.resultexchanger import entity

########################################################################
class ResultExchangerTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_1_test_record(self):
        """"""
        recorder = entity.TaskIdCacher('test1.db')
        #recorder.push_one('1,1,2,3')
        #recorder.push_one('1,1,2,31')
        #recorder.push_one('1,1,2,32')
        #recorder.push_one('1,1,2,33')
        #recorder.push_one('1,1,2,34s')
        recorder.save()
        for i in range(3):
            self.assertNotEqual(None, recorder.peek_one())
            
    #----------------------------------------------------------------------
    def test_2_test_remove_record(self):
        """"""
        r = entity.TaskIdCacher('test1.db')
        r.remove_one('1,1,2,31')
    
    

if __name__ == '__main__':
    unittest.main()