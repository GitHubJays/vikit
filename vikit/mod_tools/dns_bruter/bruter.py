#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Brute SubDomain
  Created: 2016/12/7
"""

import unittest
import json 
import os
from os import system
from threading import Thread
from threading import Timer
from time import sleep
from pprint import pprint
from Queue import Queue

from g3ar import ThreadPool as Pool
from g3ar import DictParser
from g3ar.utils.queue_utils import async_dispatch

from guesser import check_existed
#from dict_parser import DictParser
#from thread_pool import Pool

#check_existed(subdomain, nameserver=[], timeout=5)


ROOT_PATH = os.path.dirname(__file__)
DEFAULT_DICT = './dict/subnames_largest.txt'

########################################################################
class DNSBruter(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, target, thread_max=30, nameserver=[], dict_file=None,
                 do_continue=True, session_id='dns_bruter_session', timeout=5,
                 clean_mod=True, ):
        """Constructor"""
        #
        # process params
        #
        self._timeout = timeout
        self._target = target
        self._dict_file = dict_file if dict_file else os.path.join(ROOT_PATH, 
                                                                   DEFAULT_DICT)
        self._do_continue = do_continue
        self._session_id = session_id
        self._nameservers = nameserver
        self._pool_clean_mod = clean_mod
        self._thread_max = thread_max
        
        #
        # error-ip
        #
        self._error_result = check_existed('.'.join(['abas0luatessnot',self._target]))
        self._error_ip = self._error_result.get('IP')
        
        #
        # initial components
        #
        self._pool = Pool(self._thread_max, self._pool_clean_mod)
        self._pool.start()
        
        self._dict_parser = DictParser(self._dict_file, 
                                       self._session_id,
                                       self._do_continue)
        
        self._result_queue = Queue()
        
    #----------------------------------------------------------------------
    def _start(self):
        """"""
        for prefix in self._dict_parser:
            target = '.'.join([prefix, self._target])
            while self._pool.get_task_queue().qsize() > 50:
                sleep(0.1)
            
            while self._pool.get_result_queue().qsize() > 50:
                sleep(0.1)
            
            #check_existed(target, self._nameservers, self._timeout)
            self._pool.feed(check_existed, target, self._nameservers, self._timeout)
    
    #----------------------------------------------------------------------
    def result_filter(self):
        """"""
        result = self._pool.get_result_queue()
        while True:
            while self._result_queue.qsize() > 50:
                sleep(0.1)
            
            _ret = result.get()
            if _ret.get('result').get('IP') != self._error_ip and _ret.get('result').get('IP') != '':
                self._result_queue.put(_ret)
            else:
                pass
    
    #----------------------------------------------------------------------
    def saver(self, interval=3):
        """"""
        while True:
            sleep(interval)
            self.force_save()
    
    
    #----------------------------------------------------------------------
    def force_save(self):
        """"""
        self._dict_parser.force_save()
    
    #----------------------------------------------------------------------
    def start(self):
        """"""
        saver = Thread(target=self.saver, name='saver')
        saver.daemon = True
        saver.start()
        
        starter = Thread(target=self._start, name='starter')
        starter.daemon = True
        starter.start()
        
        rfilter = Thread(target=self.result_filter, name='filter')
        rfilter.daemon = True
        rfilter.start()
        
        return self._result_queue
    

########################################################################
class BurterTester(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_dns_bruter(self):
        """"""
        burter = DNSBruter(target='uestc.edu.cn', do_continue=True)
        queuei = burter.start()
        for i in xrange(15):
            print queuei.get()
        
        burter.force_save()
        
    
if __name__ == '__main__':
    unittest.main()