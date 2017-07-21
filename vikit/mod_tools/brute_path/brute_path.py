#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Brute Web Path
  Created: 2016/12/14
"""

import os
import time
import unittest
from urlparse import urljoin
from threading import Thread
from pprint import pprint

from dict_parser import DictParser
from vthu.thread_pool import Pool
from lib.connect import request_page
 


########################################################################
class BrutePath():
    """"""

    #----------------------------------------------------------------------
    def __init__(self, target, headers={}, cookie={},
                 dict_file='dicts/dir.txt', timeout=5,
                 max_pool_threads=30, session_id='default', 
                 do_continue=False):
        """Constructor"""
        self._target = target
        self._headers = headers
        self._cookie = cookie
        self._timeout = timeout
        
        self._dict_file = dict_file
        if os.path.exists(self._dict_file):
            pass
        else:
            self._dict_file = os.path.join(
                os.path.abspath(os.path.dirname(__file__)),
                self._dict_file
            )
            assert os.path.exists(self._dict_file)
        
        self._dict_parser = DictParser(self._dict_file, session_id, do_continue)
        
        self._nopage_status_code = 404
        self._max_pool_threads = max_pool_threads
        self._pool = Pool(self._max_pool_threads)
        
        #build-in
        self._finished = False
        
    
    #----------------------------------------------------------------------
    def __del__(self):
        """"""
        try:
            self._pool.stop()
            del self._dict_parser
        except:
            pass
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        self._pool.start()
        
        ret = Thread(name='task_dispachter', target=self._start)
        ret.daemon = True
        ret.start()
        
        return self._pool.get_result_queue()
    
    #----------------------------------------------------------------------
    def _start(self):
        """"""
        for i in self._dict_parser:
            if self._pool.get_task_queue().qsize() > self._max_pool_threads * 3:
                time.sleep(5)
            #print '...'
            self._pool.feed(self._worker, i)
        
        self._finished = True
    
    #----------------------------------------------------------------------
    @property
    def finished(self):
        """"""
        return self._finished
        
        
    #----------------------------------------------------------------------
    def _worker(self, payload):
        """"""
        result = {}
        #print 'using ', payload
        result['payload'] = payload
        
        url = urljoin(self._target, payload)
        result['url'] = url
        
        rsp = request_page(url, headers=self._headers, 
                           cookies=self._cookie,
                           timeout=self._timeout)
        
        #print 'got result'
        if rsp != None:
            existed = self._process_response(rsp)
        else:
            existed = None
        
        result['existed'] = existed
        #print result
        return result
        
    #----------------------------------------------------------------------
    def _process_response(self, rsp):
        """"""
        #print rsp.status_code
        if rsp.status_code == self._nopage_status_code:
            return False
        elif rsp.status_code == 200 or rsp.status_code == 403:
            return True
        else:
            return None
        
        




########################################################################
class TestBruter(unittest.case.TestCase):
    """"""
    #----------------------------------------------------------------------
    def test_request_page(self):
        """"""
        rsp = request_page(url='https://blog.tbis.me/bbs/leadbbs/manage/')
        print rsp
        

    #----------------------------------------------------------------------
    def test_basic_bruter(self):
        """Constructor"""
        bruter = BrutePath(target='https://blog.tbis.me/bbs/leadbbs/manage/')
        result_queue = bruter.start()
        for i in xrange(10):
            ret = result_queue.get()
            if ret['state'] == False:
                print ret['exception']
            #print 'result', ret
            #print ret
        
    
    

if __name__ == '__main__':
    unittest.main()