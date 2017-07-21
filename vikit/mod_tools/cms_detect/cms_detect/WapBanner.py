import json
import re
import warnings
import os
import logging
import pkgutil
import pkg_resources
import sys
import requests
import hashlib
import cookielib
import ssl 


import argparse
from multiprocessing.dummy import Pool

from bs4 import BeautifulSoup

logger = logging.getLogger(name=__name__)
logging.captureWarnings(True)


class WappalyzerError(Exception):
    """
    Raised for fatal Wappalyzer errors.
    """
    pass


class WebPage(object):
    """
    Simple representation of a web page, decoupled
    from any particular HTTP library's API.
    """

    def __init__(self, url, html, headers):
        """
        Initialize a new WebPage object.

        Parameters
        ----------

        url : str
            The web page URL.
        html : str
            The web page content (HTML)
        headers : dict
            The HTTP response headers
        """
        self.url = url
        self.html = html
        self.headers = headers
        self.version = ""
        self.versions = []
        self.confidence = {}
        self.confidenceTotal = 0;

        try:
            self.headers.keys()
        except AttributeError:
            raise ValueError("Headers must be a dictionary-like object")

        self._parse_html()

    def _parse_html(self):
        """
        Parse the HTML with BeautifulSoup to find <script> and <meta> tags.
        """
        self.parsed_html = soup = BeautifulSoup(self.html)
        self.scripts = [script['src'] for script in
                        soup.findAll('script', src=True)]
        self.meta = {
            meta['name'].lower():
                meta['content'] for meta in soup.findAll(
                    'meta', attrs=dict(name=True, content=True))
        }

    @classmethod
    def new_from_url(cls, url, verify=False):
        """
        Constructs a new WebPage object for the URL,
        using the `requests` module to fetch the HTML.

        Parameters
        ----------

        url : str
        verify: bool
        """
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'}
        response = requests.get(url, headers=headers, verify=verify, timeout=5)
        return cls.new_from_response(response)        
        #if cls.cookies:
            #response = requests.get(url, verify=verify, timeout=2.5, headers=headers, cookies= cls.cookies)
            #return cls.new_from_response(response)
        #else:    
            #response = requests.get(url, verify=verify, timeout=2.5, headers=headers)
            #return cls.new_from_response(response)


    @classmethod
    def follow_from_url(self, url, cookie):
        """
        Constructs a new WebPage object for the URL,
        using the `requests` module to fetch the HTML.

        Parameters
        ----------

        url : str
        verify: bool
        """
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36'}
        response = requests.get(url, headers=headers, verify=verify, timeout=5, cookies=cookie)
        return cls.new_from_response(response)        
        #if cls.cookies:
            #response = requests.get(url, verify=verify, timeout=2.5, headers=headers, cookies= cls.cookies)
            #return cls.new_from_response(response)
        #else:    
            #response = requests.get(url, verify=verify, timeout=2.5, headers=headers)
            #return cls.new_from_response(response)


    @classmethod
    def new_from_response(cls, response):
        """
        Constructs a new WebPage object for the response,
        using the `BeautifulSoup` module to parse the HTML.

        Parameters
        ----------

        response : requests.Response object
        """
        return cls(response.url, html=response.text, headers=response.headers)
    
class Wappalyzer(object):
    """
    Python Wappalyzer driver.
    """
    def __init__(self, categories, apps):
        """
        Initialize a new Wappalyzer instance.

        Parameters
        ----------

        categories : dict
            Map of category ids to names, as in apps.json.
        apps : dict
            Map of app names to app dicts, as in apps.json.
        """
        self.categories = categories
        self.apps = apps

        for name, app in self.apps.items():
            self._prepare_app(app)

    @classmethod
    def latest(cls, apps_file=None):
        """
        Construct a Wappalyzer instance using a apps db path passed in via
        apps_file, or alternatively the default in data/apps.json
        """
        if apps_file:
            with open(apps_file, 'r') as fd:
                obj = json.load(fd)
        else:
            obj = json.loads(pkg_resources.resource_string(__name__, "apps.json"))

        return cls(categories=obj['categories'], apps=obj['apps'])

    def _prepare_app(self, app):
        """
        Normalize app data, preparing it for the detection phase.
        """

        # Ensure these keys' values are lists
        for key in ['url', 'html', 'script', 'implies']:
            try:
                value = app[key]
            except KeyError:
                app[key] = []
            else:
                if not isinstance(value, list):
                    app[key] = [value]

        # Ensure these keys exist
        for key in ['headers', 'meta']:
            try:
                value = app[key]
            except KeyError:
                app[key] = {}

        # Ensure the 'meta' key is a dict
        obj = app['meta']
        if not isinstance(obj, dict):
            app['meta'] = {'generator': obj}

        # Ensure keys are lowercase
        for key in ['headers', 'meta']:
            obj = app[key]
            app[key] = {k.lower(): v for k, v in obj.items()}

        # Prepare regular expression patterns
        for key in ['url', 'html', 'script']:
            #try:
                #value = app[key]
            #except KeyError:
                #app[key] = {}            
            app[key] = [self._prepare_pattern(pattern) for pattern in app[key]]

        for key in ['headers', 'meta']:
            #try:
                #value = app[key]
            #except KeyError:
                #app[key] = {}            
            obj = app[key]
            for name, pattern in obj.items():
                obj[name] = self._prepare_pattern(obj[name])
                
        for key in ['md5']:
            try:
                value = app[key]
            except KeyError:
                app[key] = {}
                
        for keyword in ['keyword']:
            try:
                value = app[key]
            except KeyError:
                app[key] = {}

    def _prepare_pattern(self, pattern):
        """
        Strip out key:value pairs from the pattern and compile the regular
        expression.
        """
        regex, _, rest = pattern.partition('\\;')
        try:
            return re.compile(regex, re.I)
        except re.error as e:
            warnings.warn(
                "Caught '{error}' compiling regex: {regex}"
                .format(error=e, regex=regex)
            )
            # regex that never matches:
            # http://stackoverflow.com/a/1845097/413622
            return re.compile(r'(?!x)x')

    #def _version_confidence(self, parttern, text):
        #"""
        #determine the cms version or confidence.
        #"""
        #re = self._prepare_pattern(parttern)
        #if re.search(text):
            #if parttern.find("\\;version:\\1") != -1:
                
            #elif parttern.find("\\;confidence:\\1") != -1:
                
            #else:
                
            #return True        

    def _has_app(self, app, webpage):
        """
        Determine whether the web page matches the app signature.
        """
        # Search the easiest things first and save the full-text search of the
        # HTML for last
        for regex in app['url']:
            if regex.search(webpage.url):
                return True            
            #if regex.find("\\;") == -1:
                #if regex.search(webpage.url):
                    #return True
            #else:
                #re = self._prepare_pattern(regex)
                #if re.search(webpage.url):
                    #return True
                
        for name, regex in app['headers'].items():
            if name in webpage.headers:
                content = webpage.headers[name]
                if regex.search(content):
                    return True                  
                #if regex.find("\\;") == -1:
                    #if regex.search(content):
                        #return True                    
                #else:  
                    #re = self._prepare_pattern(regex)
                    #if re.search(content):
                        #return True

        for regex in app['script']:
            #print regex
            for script in webpage.scripts:
                if regex.search(script):
                    return True                
                #if regex.find("\\;") == -1:
                    #if regex.search(script):
                        #return True
                #else:    
                    #re = self._prepare_pattern(regex)
                    #if re.search(script):
                        #return True

        for name, regex in app['meta'].items():
            if name in webpage.meta:
                content = webpage.meta[name]
                if regex.search(content):
                    return True                
                #if regex.find("\\;") == -1:
                    #if regex.search(content):
                        #return True
                #re = self._prepare_pattern(regex)
                #if re.search(content):
                    #return True

        for regex in app['html']:
            if regex.search(webpage.html):
                return True            
            #if regex.find("\\;") == -1:
                #if regex.search(webpage.html):
                    #return True
            #else:
                #re = self._prepare_pattern(regex)
                #if re.search(webpage.html):
                    #return True
            

    def _has_cms(self, app, webpage):
        """
        Determine cms by md5 and keyword
        """
        try:
            for path, md5 in app['md5'].items():
                if self._check_md5(webpage.url + path[1:], md5):
                    return True
                
            for path, keyword in app['keyword'].items():
                if self._check_keyword(webpage.url + path[1:], keyword):
                    return True
        except Exception, ex:
            return False

    def _check_md5(self, url, md5):
        """
        check file md5
        """
        try:
            page = WebPage.new_from_url(url)
            content = page.html.encode("utf-8")
            m = hashlib.md5()
            n = hashlib.md5(content).hexdigest()
            if md5 != n:
                return False
            else:
                return True
        except Exception, ex:
            return False
        
    def _check_keyword(self, url, keyword):
        """
        check file keyword
        """
        try:
            page = WebPage.follow_from_url(url)
            if keyword.search(page.html):
                return True
        except Exception, ex:
                    return False            
        
    def _get_implied_apps(self, detected_apps):
        """
        Get the set of apps implied by `detected_apps`.
        """
        def __get_implied_apps(apps):
            _implied_apps = set()
            for app in apps:
                try:
                    _implied_apps.update(set(self.apps[app]['implies']))
                except KeyError:
                    pass
            return _implied_apps

        implied_apps = __get_implied_apps(detected_apps)
        all_implied_apps = set()

        # Descend recursively until we've found all implied apps
        while not all_implied_apps.issuperset(implied_apps):
            all_implied_apps.update(implied_apps)
            implied_apps = __get_implied_apps(all_implied_apps)

        return all_implied_apps

    def get_categories(self, app_name):
        """
        Returns a list of the categories for an app name.
        """
        cat_nums = self.apps.get(app_name, {}).get("cats", [])
        cat_names = [self.categories.get("%s" % cat_num, "")
                     for cat_num in cat_nums]

        return cat_names

    def analyze(self, webpage):
        """
        Return a list of applications that can be detected on the web page.
        """
        
        detected_apps = set()

        for app_name, app in self.apps.items():
            if self._has_app(app, webpage):
                detected_apps.add(app_name)

        detected_apps |= self._get_implied_apps(detected_apps)

        return detected_apps

    def analyze_with_categories(self, webpage):
        detected_apps = self.analyze(webpage)
        categorised_apps = {}

        for app_name in detected_apps:
            cat_names = self.get_categories(app_name)
            if cat_names:
                categorised_apps[cat_names[0]]=app_name    

        if not categorised_apps.has_key("cms"):
            for app_name, app in self.apps.items():
                if self._has_cms(app, webpage):
                    categorised_apps['cms'] = app_name
                    return categorised_apps

        return categorised_apps

import urlparse

def worker(url, wappalyzer):
    if not url.startswith('http'):
        url = 'http://' + url
    webpage = WebPage.new_from_url(url)
    ret = wappalyzer.analyze_with_categories(webpage)
    ret['target'] = webpage.url
    #print json.dumps(ret)
    return ret

def app_detect(url):
    wappalyzer = Wappalyzer.latest()
    return worker(url, wappalyzer)

if __name__ == '__main__':
    """
    FAILED LIST:
    southidc
    """
    ret = cms_detect(url='https://blog.tbis.me')
    #print ret
    for i in ret.items():
        print i
    
    """
    wappalyzer = Wappalyzer.latest()
    
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-u', '--URL', help='URL')
    parser.add_argument('-f', '--file_path', help='file path.')
    args = parser.parse_args()
    url = args.URL
    file_path = args.file_path
    if url:
        worker(url, wappalyzer)
    elif os.path.isfile(file_path):
        pool = Pool(5)
        with open(file_path, 'rb') as f:
            for url in f:
                pool.apply_async(worker, args=(url.strip(), wappalyzer,))
        pool.close()
        pool.join()
    """
    
    
    
   
