#  -*- coding: utf-8 -*-

import sys
import os
sys.path.append(os.path.dirname(__file__))


from wafw00f.wafw00f import WafDetect
import requests
CHECK_WAF_INFO = {}

class checkWaf(object):
    """docstring for checkWaf"""
    allow_redirects = True  # 是否允许URL重定向
    access_status_code = [200,301]
    proxy = {}

    def __init__(self,url):
        super(checkWaf, self).__init__()
        self.url = url
        self.headers = {}

        
    def run(self):
        result = WafDetect().run(self.url,self.headers)
        CHECK_WAF_INFO['result'] = result
        CHECK_WAF_INFO['target'] = self.url


        return CHECK_WAF_INFO
        
if __name__ == '__main__':
    def print_(info):
        print info
    url = 'http://www.telnote.cn/'
    print checkWaf(url).run()