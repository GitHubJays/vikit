#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Parse Single Page
  Created: 2016/11/29
"""

import unittest
import chardet
#import ghost
import traceback
import bs4
import urlparse
from pprint import pprint

from requests import Session
from requests import Request

import warnings
warnings.filterwarnings(action='ignore')

#----------------------------------------------------------------------
def get_encode_type(text):
    """"""
    if isinstance(text, str):
        return chardet.detect(text)['encoding']
    else:
        return chardet.detect(text)['encoding']
    

########################################################################
class LinkParser(object):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, url, timeout, load_js, 
                 headers={}, cookie={}, method="GET",
                 post_data={},
                 depth=-1, cache=False,
                 encoding='utf-8'):
        """Constructor"""
        self.url = url
        
        assert isinstance(timeout, int)
        self.timeout = timeout
        
        assert isinstance(load_js, bool)
        self.load_js = load_js
        
        assert isinstance(cache, bool)
        self.cache = cache
        
        assert isinstance(depth, int)
        self.depth = depth
    
        self.post_data = {}
        self.method = method
        self.headers = headers
        self.cookie = cookie
        
        #::
        self.encoding = encoding
    
        #build-in
        self.url_links = {}
        self.html_content = ""
        
        self.url_links['a'] = []
        self.url_links['link'] = []
        self.url_links['img'] = []
        self.url_links['script'] = []
    
    #----------------------------------------------------------------------
    def _req_static_page(self):
        """"""
        s = Session()
        r = Request(method=self.method, url=self.url, headers=self.headers,
                    data=self.post_data, cookies=self.cookie)
        
        r = r.prepare()
        
        self.response = None
        
        try: 
            self.response = s.send(r, timeout=self.timeout)
        except:
            pass
        
        if self.response == None:
            return ""
        else:
            raw = self.response.text.encode('utf-8')
            encode_type = get_encode_type(raw)
            self.html_content = raw.decode(encode_type).encode(self.encoding)
            return self.html_content
    
    #----------------------------------------------------------------------
    def _req_dynamic_page(self):
        """"""
        rsp = None   
    
        gh = ghost.Ghost()
        with gh.start(download_images=False) as session:
            _ = session.open(address=self.url, method=self.method, headers=self.headers, 
                               timeout=self.timeout)
            rsp = _[0]
            
        if rsp != None:
            raw = rsp.content.__str__()
            #print raw
            encode_type = get_encode_type(raw)
            self.html_content = raw.decode(encode_type, 'ignore').encode(self.encoding, 'ignore')
            return self.html_content
        else:
            self.html_content = ''
            return self.html_content
        
    #----------------------------------------------------------------------
    def _handle_back_path(self):
        """"""
        #print link
        link_split = link.split('/')
        back_count = link_split.count('..')
        o = urlparse.urlparse(url)
        url_path = o[2]
        pathlist = []
        #print url_path
        #if url_path.endswith('/'):
        pathlist = url_path.split('/')[:-1]
        ##else:
            #pathlist = url_path.split('/')[:-1]
        
        new_item = ''
        for i in link_split:
            if i == '' or i == '..':
                pass
            else:
                new_item = new_item + '/' + i
        
        
        new_link_path = pathlist[:-back_count]
        new_path = '/'.join(new_link_path) + new_item
        new_link = o[0]+'://'+o[1]+new_path+o[3]+o[4]+o[5]
        #print url
        #print new_link
        return new_link       
    
    #----------------------------------------------------------------------
    def complet_url(self, link):
        """"""
        return urlparse.urljoin(base=self.url, url=link)
        

    #----------------------------------------------------------------------
    def get_result(self):
        """"""
        if self.html_content == '':
            if self.load_js:
                self.html_content = self._req_dynamic_page()
            else:
                self.html_content = self._req_static_page()
                
        self.soup = bs4.BeautifulSoup(self.html_content)
            
        self.result = {}
        
        self.get_tag_a()
        self.get_tag_link()
        self.get_tag_img()
        self.get_tag_script()
        
        # links remove-repeat
        for child in self.url_links.keys():
            self.url_links[child] = list(set(self.url_links[child]))
        
        self.result[self.url] = self.url_links
        
        return self.result
    
    def get_tag_a(self):
        """"""
        # 处理A链接
        for tag in self.soup.find_all('a'):
            if tag.attrs.has_key('href'):
                #print tag['href']
                link = tag.attrs['href']
                # link = urlparse.urldefrag(tag.attrs['href'])[0] # 处理掉#tag标签信息
                complet_link = self.complet_url(link.strip())
                #print complet_link
                if complet_link:
                    self.url_links['a'].append(complet_link)
        return self.url_links
    
    #----------------------------------------------------------------------
    def get_tag_link(self):
        """"""
        for tag in self.soup.find_all('link'):
            if tag.attrs.has_key('href'):
                link = tag.attrs['href']
                complet_link = self.complet_url(link.strip())
                if complet_link:
                    self.url_links['link'].append(complet_link)
        return self.url_links
    
    #----------------------------------------------------------------------
    def get_tag_img(self):
        """"""
        for tag in self.soup.find_all('img'):
            if tag.attrs.has_key('src'):
                link = tag.attrs['src']
                complet_link = self.complet_url(link.strip())
                if complet_link:
                    self.url_links['img'].append(complet_link)
        return self.url_links  
    
    #----------------------------------------------------------------------
    def get_tag_script(self):
        """"""
        for tag in self.soup.find_all('script'):
            if tag.attrs.has_key('src'):
                link = tag.attrs['src']
                complet_link = self.complet_url(link.strip())
                if complet_link:
                    self.url_links['script'].append(complet_link)
        return self.url_links        
        

########################################################################
class LinkParserTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def runTest(self):
        """"""
        pprint('TEST Link Parser')
        target = 'https://blog.tbis.me/'
        pageparser = LinkParser(url=target, load_js=True, 
                                timeout=10)
    
        result = pageparser.get_result()[target]
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result.has_key('a'))
        self.assertTrue(result.has_key('link'))
        self.assertTrue(result.has_key('img'))
        self.assertTrue(result.has_key('script'))
        pprint(result)
        
if __name__ == '__main__':
    #unittest.main()
    
    _ = LinkParser(url='https://blog.tbis.me/', load_js=False,
               timeout=100)
    
    result = _.get_result()
    pprint(result)