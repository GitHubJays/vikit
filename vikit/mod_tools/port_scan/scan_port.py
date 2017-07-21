#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Quick Scan Port
  Created: 2016/12/18
"""

import unittest
import time
import sys
from pprint import pprint
from threading import Thread

#from thread_pool import Pool
from g3ar import ThreadPool as Pool
from nmaplib.nmap import PortScanner
from nmaplib import nmap_options
from nmaplib.nmap_options import generate_arguments




#----------------------------------------------------------------------
def scan(target, ports=None, timeout=10,
         arguments=nmap_options.DEFAULT_ARUGUMENTS_WITH_VERSION_DETECTION_PRO,
         extra=None):
    """Scan Port Use nmap
    
    Params:
        target: :str: the target host you want to scan.
        ports: :str: the port you want to scan.
        timeout: :int: the seconds for every request
        arguments: :str: the default scan arguments.
        extra: :str: Extra scan option
    
    Returns:
        the scaninfo and result will be returned. And the state is True for 
        success, False for a failure.
        
        Example:
        {'result': {'ports': {'tcp': {80: {'conf': '10',
                                           'cpe': 'cpe:/a:igor_sysoev:nginx:1.6.2',
                                           'extrainfo': '',
                                           'name': 'http',
                                           'product': 'nginx',
                                           'reason': 'syn-ack',
                                           'state': 'open',
                                           'version': '1.6.2'}}},
                    },
         'target': '45.78.6.64',
         'state': True}
         """
    result = {}
    result['target'] = target
    result['state'] = False
    _result = result['result'] = {}
    
    assert (',' or '/') not in target, 'The target must be one target not many targets'
    assert isinstance(timeout, int), 'The timeout shuold be a int for seconds'
    arguments = generate_arguments(arguments, '--max-rtt-timeout {0}ms'.format(timeout*1000))
    if extra:
        arguments = generate_arguments(arguments, extra)
    else:
        pass
    
    try:
        portscanner = PortScanner()
        ret = portscanner.scan(hosts=target, ports=ports,
                                  arguments=arguments)
    
        #pprint(ret)
        
        #scaninfo = _result['scaninfo'] = {}
        #scaninfo['cmdline'] = ret['nmap']['command_line']
        #scaninfo['scaninfo'] = ret['nmap']['scaninfo']
        #scaninfo['starttime'] = ret['nmap']['scanstats']['timestr']
        #scaninfo['elapsed'] = ret['nmap']['scanstats']['elapsed']
        
        #del scaninfo
        
        port_info = _result['ports'] = {}
        _ = ret['scan'][target]
        if _.has_key('tcp'):
            port_info['tcp'] = _['tcp']
        elif _.has_key('udp'):
            port_info['udp'] = _['udp']
        result['state'] = True
    except:
        result['state'] = False
        
    result_return = result.copy()
    del result
    
    return result_return

########################################################################
class QuickPortScanner(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, target, 
                 ports=None, 
                 extra_arg=None, 
                 default_arguments=None,
                 timeout=10, 
                 max_pool_threads=30):
        """Constructor"""
        self._default_arg = nmap_options.DEFAULT_ARUGUMENTS_WITH_VERSION_DETECTION_PRO \
            if not default_arguments else default_arguments
        self._extra_arg = extra_arg if extra_arg else None
        self._timeout = timeout
        self._target = target
        
        #
        # Process Ports
        #
        if isinstance(ports, int):
            self._ports_raw = str(ports)
        elif isinstance(ports, str):
            self._ports_raw = ports
        else:
            self._ports_raw = ','.join(map(lambda x: str(x), nmap_options.ALL_KNOWN_PORT))
            
        self._ports = self._process_ports_raw(self._ports_raw)\
            if self._process_ports_raw(self._ports_raw) else nmap_options.ALL_KNOWN_PORT
        
        self._max_pool_threads = max_pool_threads
        
        self._pool = Pool(self._max_pool_threads)
        self._result_queue = None
        
    #----------------------------------------------------------------------
    def _dispatcher(self):
        """"""
        for i in self._ports:
            port = str(i)
            self._pool.feed(scan, target=self._target,
                            ports=port,
                            timeout=self._timeout,
                            arguments=self._default_arg,
                            extra=self._extra_arg)
            
            if self._pool.get_task_queue().qsize() > 2 * self._max_pool_threads:
                time.sleep(5)
            else:
                pass
        
    #----------------------------------------------------------------------
    def start(self):
        """"""
        self._pool.start()
        ret = Thread(name='portscanner_task_dispatcher',
                     target=self._dispatcher)
        ret.daemon = True
        ret.start()
        
        self._result_queue = self._pool.get_result_queue()
        return self._result_queue
        
    #----------------------------------------------------------------------
    def _process_ports_raw(self, raw):
        """"""
        try:
            if '-' in raw:
                p = raw.split('-')
                ports = range(int(p[0].strip()), int(p[1].strip()))
            elif ',' in raw:
                p = map(lambda x: int(x.strip()), raw.split(','))
            else:
                p = list(int(raw.strip()))
            
            return p
        except:
            return None
    
    #----------------------------------------------------------------------
    @property
    def task_count(self):
        """"""
        return len(self._ports)
        

########################################################################
class ScanPortTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_scan_port_basic_api(self):
        """"""
        portscan_worker = PortScanner()
        ret = portscan_worker.scan(hosts='127.0.0.1', ports='80')
        #pprint(ret)
    
    #----------------------------------------------------------------------
    def test_scan_simple(self):
        """"""
        et = scan(target='45.78.6.64', ports='80', timeout=10)
        pprint(et)
        
    #----------------------------------------------------------------------
    def test_quickportscanner(self):
        """"""
        qps = QuickPortScanner(target='127.0.0.1')
        result = qps.start()
        count = 0
        print time.time()
        while True:
            ret = result.get()
            count = count + 1
            pprint(ret)
            if count == qps.task_count:
                break
        print time.time()
        pprint('Success!')
            
        
if __name__ == '__main__':
    unittest.main()
    
    #
    #1482150793-1482150864
    #