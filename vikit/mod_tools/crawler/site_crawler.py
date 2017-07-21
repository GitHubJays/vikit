#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Site Crawler
  Created: 2016/11/30
"""

import unittest
import urlparse
#from Queue import Queue
from pprint import pprint
from time import time
from time import sleep
from multiprocessing import Queue
from thread_utils import Pool
from thread_utils import start_thread
from page_parser import LinkParser


########################################################################
class Crawler(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, start_url, max_depth=3,
                 timeout=10, thread_max=30,
                 method='GET', headers={}, cookie={},
                 post_data={}, cache=False,
                 encoding="utf-8", load_js=False,
                 mode='thread'):
        """Constructor"""
        self.mode = mode
        self.timeout = timeout
        self.start_url = start_url
        
        self.netloc = urlparse.urlparse(self.start_url).netloc
        
        assert isinstance(max_depth, int)
        self.max_depth=max_depth
        self.load_js = load_js
        self.headers = headers
        self.cookie = cookie
        self.method = method
        self.thread_max = thread_max
        
        self.post_data = post_data
        
        self.cache = cache
        self.encoding = encoding
        
        #build-in
        self._depth_url_table = {}
        self._depth_resource_table = {}
        
        self._initial_config()
        self._visited_url = []
        self.result_queue = Queue()
        self._finished = False
        self.current_pool = None
        
    #----------------------------------------------------------------------
    def _initial_config(self):
        """"""
        self._depth_url_table[0] = [self.start_url]
         
    #----------------------------------------------------------------------
    def _get_url_by_depth(self, depth):
        """"""
        if self._depth_url_table.has_key(depth):
            return tuple(self._depth_url_table[depth])
        else:
            return tuple([])
        
    #----------------------------------------------------------------------
    def _worker(self, *args, **params):
        """"""
        linkparser = LinkParser(**params)
        #pprint(params['url'])
        return linkparser.get_result()
    
    #----------------------------------------------------------------------
    def _crawler_by_depth(self, depth):
        """"""
        if depth:
            pass
        else:
            depth = self.max_depth
            
        self._finished = False
        start_thread(self.heartbeats)
        
        for current_depth in xrange(depth):
            result = {}
            #pprint(current_depth)
            nxt_depth = current_depth + 1
            
            task_count = len(self._depth_url_table[current_depth])
            
            self.current_pool = Pool(thread_max=self.thread_max,
                                     mode=self.mode)

            params = {}
            params['timeout'] = self.timeout
            params['headers'] = self.headers
            params['cookie'] = self.cookie
            params['method'] = self.method
            params['post_data'] = self.post_data
            params['depth'] = current_depth
            params['load_js'] = self.load_js
            params['encoding'] = self.encoding
            params['cache'] = self.cache

            for i in self._depth_url_table[current_depth]:
                params['url'] = i
                #pprint(i)
                self.current_pool.add_task(self._worker, **params.copy())
            
            _queue = self.current_pool.run()
        
            #_ = 0
            for _ in xrange(task_count):
                _r = _queue.get()
                #pprint(result)
                self._process_linkparser_result(_r, nxt_depth)
            
            result['depth'] = nxt_depth
            if self._depth_resource_table.has_key(nxt_depth):
                result['resources'] = self._depth_resource_table[nxt_depth]
            else:
                result['resources'] = self._depth_resource_table[nxt_depth] = []
            
            if self._depth_url_table.has_key(nxt_depth):
                result['urls'] = self._depth_url_table[nxt_depth]
            else:
                result['urls'] = self._depth_url_table[nxt_depth] = []
            result['tag'] = 'current_depth_result'
            self.result_queue.put(result.copy())
            #pprint(result)
        
        self._finished = True
        result = {}
        result['tag'] = 'final_result'
        result['url_table'] = self._depth_url_table
        result['resource_table'] = self._depth_resource_table
        self.result_queue.put(result)
                
    #----------------------------------------------------------------------
    def _process_linkparser_result(self, result_from_worker, nxt_depth):
        """"""
        ret = result_from_worker
        values = ret.values()[0]
        if self._depth_url_table.has_key(nxt_depth):
            pass
        else:
            self._depth_url_table[nxt_depth] = []
            
        if self._depth_resource_table.has_key(nxt_depth):
            pass
        else:
            self._depth_resource_table[nxt_depth] = []
            
        for i in values['a']:
            if i in self._visited_url:
                pass
            else:
                if self.netloc != urlparse.urlparse(i).netloc:
                    pass
                else:
                    self._visited_url.append(i)
                    self._depth_url_table[nxt_depth].append(i)
        
        for i in values['link'] + values['img'] + values['script']:
            if i in self._visited_url:
                pass
            else:
                self._visited_url.append(i)
                self._depth_resource_table[nxt_depth].append(i)
        
    #----------------------------------------------------------------------
    def async_run(self, depth=None):
        """"""
        if depth:
            pass
        else:
            depth = self.max_depth
            
        start_thread(self._crawler_by_depth, depth)
        return self.result_queue

    #----------------------------------------------------------------------
    def get_result(self):
        """"""
        pass
    
    #----------------------------------------------------------------------
    def heartbeats(self):
        """"""
        while self._finished == False:
            sleep(30)
            try:
                result = {}
                result['tag'] = 'heartbeats'
                result['visited_url_count'] = {}
                for i in self._depth_url_table.items():
                    result['visited_url_count'][i[0]] = len(i[1])
                result['current_thread_count'] = self.current_pool.current_thread_count
                self.result_queue.put(result)
            except:
                pass
        
########################################################################
class CrawlerTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """Constructor"""

        cralwer = Crawler(start_url='https://blog.tbis.me/',
                          mode='process', thread_max=5)
        
        result_queue = cralwer.async_run(depth=2)
        
        pprint(time())
        while True:
            try:
                result = result_queue.get(timeout=40)
            except:
                break
            if result['tag'] == 'current_depth_result':
                self.assertTrue(result.has_key('depth'))
                self.assertTrue(result.has_key('resources'))
                self.assertTrue(result.has_key('urls'))
                pprint('DEPTH:    ') 
                pprint(result['depth'])
                pprint('COUNT_URL:')
                pprint(len(result['urls']))
                pprint(time())
                pprint(result)
            else:
                pprint(result)
                pprint(time())

if __name__ == '__main__':
    """

C:\Users\villa\OneDrive\github\TDD\tx\refact_tx\plugins\info_collect\crawler>python site_crawler.py
1480472619.546
'DEPTH:    '
1
'COUNT_URL:'
46
1480472620.968
'DEPTH:    '
2
'COUNT_URL:'
257
1480472669.254
'DEPTH:    '
3
'COUNT_URL:'
222
1480473077.919
.
----------------------------------------------------------------------
Ran 1 test in 458.373s

OK

"""
    unittest.main()