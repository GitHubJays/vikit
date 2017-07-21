#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Connect
  Created: 2016/12/14
"""

import unittest
from pprint import pprint

import requests
from requests import Session
from requests import Request


#----------------------------------------------------------------------
def request_page(url, headers={}, cookies={}, timeout=5):
    """"""
    req = Request(method='get', url=url,
                  headers=headers,
                  cookies=cookies,)
    reqd = req.prepare()
    
    session = Session()
    try:
        rsp = session.send(reqd, allow_redirects=False, timeout=timeout)
        return rsp
    except:
        return None


#----------------------------------------------------------------------
def existed(rsp, no_page_status_code=404):
    """Test the response, check the target path existed
    
    Returns:
        the info of rsp
        :type: Dict
        Example:
            {'existed': True, 
            'status_code': 200, 
            'url': u'http://127.0.0.1/hackphp/'}"""
    result = {}
    if rsp != None:
        result['url'] = rsp.url
        result['status_code'] = rsp.status_code
        if rsp.status_code == no_page_status_code:
            result['existed'] = False
        elif rsp.status_code == 200 or no_page_status_code == 403:
            result['existed'] = True
        else:
            result['existed'] = None
        
        return result
    else:
        return None
    

########################################################################
class RequestPageTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_request_page(self):
        """Constructor"""
        rsp = request_page(url='http://127.0.0.1/no-such-path/', headers={}, cookies={},
                           timeout=5)
        print rsp.text
        print rsp.url
        print rsp.status_code 
    #----------------------------------------------------------------------
    def test_exsited(self):
        """"""
        rsp = request_page('http://127.0.0.1/hackphp/')
        result = existed(rsp)
        pprint(result)
        
        
    
    

if __name__ == '__main__':
    unittest.main()