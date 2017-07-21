#coding:utf-8
import os
import sys
sys.path.append('../')

try:
    import httplib
except ImportError:
    import http.client as httplib
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.parse import quote, unquote
from optparse import OptionParser
import logging
import sys
import random

#currentDir = os.getcwd()
#scriptDir = os.path.dirname(sys.argv[0]) or '.'
#os.chdir(scriptDir)

from lib.evillib import oururlparse, scrambledheader, waftoolsengine
from manager import load_plugins

class RequestBlocked(Exception):
    pass

class WafW00F(waftoolsengine):
    """
    WAF detection tool
    """

    AdminFolder = '/Admin_Files/'
    xssstring = '<script>alert(1)</script>'
    dirtravstring = '../../../../etc/passwd'
    cleanhtmlstring = '<invalid>hello'
    isaservermatch = [
        'Forbidden ( The server denied the specified Uniform Resource Locator (URL). Contact the server administrator.  )',
        'Forbidden ( The ISA Server denied the specified Uniform Resource Locator (URL)']

    def __init__(self, target='www.microsoft.com', port=80, ssl=False,
                 debuglevel=0, path='/', followredirect=True, extraheaders={}, proxy=False):
        """
        target: the hostname or ip of the target server
        port: defaults to 80
        ssl: defaults to false
        """
        self.log = logging.getLogger('wafw00f')
        waftoolsengine.__init__(self, target, port, ssl, debuglevel, path, followredirect, extraheaders, proxy)
        self.knowledge = dict(generic=dict(found=False, reason=''), wafname=list())

    def normalrequest(self, usecache=True, cacheresponse=True, headers=None):
        return self.request(usecache=usecache, cacheresponse=cacheresponse, headers=headers)

    def normalnonexistentfile(self, usecache=True, cacheresponse=True):
        path = self.path + str(random.randrange(1000, 9999)) + '.html'
        return self.request(path=path, usecache=usecache, cacheresponse=cacheresponse)

    def unknownmethod(self, usecache=True, cacheresponse=True):
        return self.request(method='OHYEA', usecache=usecache, cacheresponse=cacheresponse)

    def directorytraversal(self, usecache=True, cacheresponse=True):
        return self.request(path=self.path + self.dirtravstring, usecache=usecache, cacheresponse=cacheresponse)

    def invalidhost(self, usecache=True, cacheresponse=True):
        randomnumber = random.randrange(100000, 999999)
        return self.request(headers={'Host': str(randomnumber)})

    def cleanhtmlencoded(self, usecache=True, cacheresponse=True):
        string = self.path + quote(self.cleanhtmlstring) + '.html'
        return self.request(path=string, usecache=usecache, cacheresponse=cacheresponse)

    def cleanhtml(self, usecache=True, cacheresponse=True):
        string = self.path + self.cleanhtmlstring + '.html'
        return self.request(path=string, usecache=usecache, cacheresponse=cacheresponse)

    def xssstandard(self, usecache=True, cacheresponse=True):
        xssstringa = self.path + self.xssstring + '.html'
        return self.request(path=xssstringa, usecache=usecache, cacheresponse=cacheresponse)

    def protectedfolder(self, usecache=True, cacheresponse=True):
        pfstring = self.path + self.AdminFolder
        return self.request(path=pfstring, usecache=usecache, cacheresponse=cacheresponse)

    def xssstandardencoded(self, usecache=True, cacheresponse=True):
        xssstringa = self.path + quote(self.xssstring) + '.html'
        return self.request(path=xssstringa, usecache=usecache, cacheresponse=cacheresponse)

    def cmddotexe(self, usecache=True, cacheresponse=True):
        # thanks j0e
        string = self.path + 'cmd.exe'
        return self.request(path=string, usecache=usecache, cacheresponse=cacheresponse)

    attacks = [cmddotexe, directorytraversal, xssstandard, protectedfolder, xssstandardencoded]

    def genericdetect(self, usecache=True, cacheresponse=True):
        knownflops = [
            ('Microsoft-IIS/7.0','Microsoft-HTTPAPI/2.0'),
        ]
        reason = ''
        reasons = ['Blocking is being done at connection/packet level.',
                   'The server header is different when an attack is detected.',
                   'The server returned a different response code when a string trigged the blacklist.',
                   'It closed the connection for a normal request.',
                   'The connection header was scrambled.'
        ]
        # test if response for a path containing html tags with known evil strings
        # gives a different response from another containing invalid html tags
        try:
            cleanresponse, _tmp = self._perform_and_check(self.cleanhtml)
            xssresponse, _tmp = self._perform_and_check(self.xssstandard)
            if xssresponse.status != cleanresponse.status:
                self.log.info('Server returned a different response when a script tag was tried')
                reason = reasons[2]
                reason += '\r\n'
                reason += 'Normal response code is "%s",' % cleanresponse.status
                reason += ' while the response code to an attack is "%s"' % xssresponse.status
                self.knowledge['generic']['reason'] = reason
                self.knowledge['generic']['found'] = True
                return True
            cleanresponse, _tmp = self._perform_and_check(self.cleanhtmlencoded)
            xssresponse, _tmp = self._perform_and_check(self.xssstandardencoded)
            if xssresponse.status != cleanresponse.status:
                self.log.info('Server returned a different response when a script tag was tried')
                reason = reasons[2]
                reason += '\r\n'
                reason += 'Normal response code is "%s",' % cleanresponse.status
                reason += ' while the response code to an attack is "%s"' % xssresponse.status
                self.knowledge['generic']['reason'] = reason
                self.knowledge['generic']['found'] = True
                return True
            response, responsebody = self._perform_and_check(self.normalrequest)
            normalserver = response.getheader('Server')
            for attack in self.attacks:
                response, responsebody = self._perform_and_check(lambda: attack(self))
                attackresponse_server = response.getheader('Server')
                if attackresponse_server:
                    if attackresponse_server != normalserver:
                        if (normalserver, attackresponse_server) in knownflops:
                            return False
                        self.log.info('Server header changed, WAF possibly detected')
                        self.log.debug('attack response: %s' % attackresponse_server)
                        self.log.debug('normal response: %s' % normalserver)
                        reason = reasons[1]
                        reason += '\r\nThe server header for a normal response is "%s",' % normalserver
                        reason += ' while the server header a response to an attack is "%s.",' % attackresponse_server
                        self.knowledge['generic']['reason'] = reason
                        self.knowledge['generic']['found'] = True
                        return True
            for attack in self.wafdetectionsprio:
                if self.wafdetections[attack](self) is None:
                    self.knowledge['generic']['reason'] = reasons[0]
                    self.knowledge['generic']['found'] = True
                    return True
            for attack in self.attacks:
                response, responsebody = self._perform_and_check(lambda: attack(self))
                for h, v in response.getheaders():
                    if scrambledheader(h):
                        self.knowledge['generic']['reason'] = reasons[4]
                        self.knowledge['generic']['found'] = True
                        return True
        except RequestBlocked:
            self.knowledge['generic']['reason'] = reasons[0]
            self.knowledge['generic']['found'] = True
            return True

        return False

    def _perform_and_check(self, request_method):
        r = request_method()
        if r is None:
            raise RequestBlocked()

        return r

    def matchheader(self, headermatch, attack=False, ignorecase=True):
        import re

        detected = False
        header, match = headermatch
        if attack:
            requests = self.attacks
        else:
            requests = [self.normalrequest]
        for request in requests:
            r = request(self)
            if r is None:
                return
            response, responsebody = r
            headerval = response.getheader(header)
            if headerval:
                # set-cookie can have multiple headers, python gives it to us
                # concatinated with a comma
                if header == 'set-cookie':
                    headervals = headerval.split(', ')
                else:
                    headervals = [headerval]
                for headerval in headervals:
                    if ignorecase:
                        if re.match(match, headerval, re.IGNORECASE):
                            detected = True
                            break
                    else:
                        if re.match(match, headerval):
                            detected = True
                            break
                if detected:
                    break
        return detected

    def matchcookie(self, match):
        """
        a convenience function which calls matchheader
        """
        return self.matchheader(('set-cookie', match))

    def isbeeware(self):
        # disabled cause it was giving way too many false positives
        # credit goes to Sebastien Gioria
        detected = False
        r = self.xssstandard()
        if r is None:
            return
        response, responsebody = r
        if (response.status != 200) or (response.reason == 'Forbidden'):
            r = self.directorytraversal()
            if r is None:
                return
            response, responsebody = r
            if response.status == 403:
                if response.reason == 'Forbidden':
                    detected = True
        return detected

    def ismodsecuritypositive(self):
        detected = False
        self.normalrequest(usecache=False, cacheresponse=False)
        randomfn = self.path + str(random.randrange(1000, 9999)) + '.html'
        r = self.request(path=randomfn)
        if r is None:
            return
        response, responsebody = r
        if response.status != 302:
            return False
        randomfnnull = randomfn + '%00'
        r = self.request(path=randomfnnull)
        if r is None:
            return
        response, responsebody = r
        if response.status == 404:
            detected = True
        return detected

    wafdetections = dict()

    # easy ones
    # lil bit more complex
    #wafdetections['BeeWare'] = isbeeware
    #wafdetections['ModSecurity (positive model)'] = ismodsecuritypositive removed for now
    wafdetectionsprio = ['Profense', 'NetContinuum', 'Incapsula WAF', 'CloudFlare', 'NSFocus', 'Safedog',
                         'Mission Control Application Shield', 'USP Secure Entry Server', 'Cisco ACE XML Gateway',
                         'Barracuda Application Firewall', 'Art of Defence HyperGuard', 'BinarySec', 'Teros WAF',
                         'F5 BIG-IP LTM', 'F5 BIG-IP APM', 'F5 BIG-IP ASM', 'F5 FirePass', 'F5 Trafficshield', 
                         'InfoGuard Airlock', 'Citrix NetScaler',
                         'Trustwave ModSecurity', 'IBM Web Application Security', 'IBM DataPower', 'DenyALL WAF',
                         'Applicure dotDefender', 'Juniper WebApp Secure',  # removed for now 'ModSecurity (positive model)',
                         'Microsoft URLScan', 'Aqtronix WebKnight', 
                         'eEye Digital Security SecureIIS', 'Imperva SecureSphere', 'Microsoft ISA Server']

    plugin_dict = load_plugins()
    result_dict = {}
    for plugin_module in plugin_dict.values():
        wafdetections[plugin_module.NAME] = plugin_module.is_waf

    def identwaf(self, findall=False):
        detected = list()

        # Check for prioritized ones first, then check those added externally
        checklist = self.wafdetectionsprio
        checklist = checklist + list(set(self.wafdetections.keys()) - set(checklist))

        for wafvendor in checklist:
            self.log.info('Checking for %s' % wafvendor)
            if self.wafdetections[wafvendor](self):
                detected.append(wafvendor)
                if not findall:
                    break
        self.knowledge['wafname'] = detected
        return detected

class WafDetect():
    def run(self,target,headers):
        if not (target.startswith('http://') or target.startswith('https://')):
            target = 'http://' + target
        pret = oururlparse(target)
        if pret is None:
            return 'url_format_error'
        (hostname, port, path, query, ssl) = pret
        attacker = WafW00F(hostname, port=port, ssl=ssl,
                           debuglevel=0, path=path,
                           followredirect=True,
                           extraheaders=headers,
                           proxy=False)
        if attacker.normalrequest() is None:
            return 'url_cannot_access'
        # if options.test:
        #     if options.test in attacker.wafdetections:
        #         waf = attacker.wafdetections[options.test](attacker)
        #         if waf:
        #             print('The site %s is behind a %s' % (target, options.test))
        #         else:
        #             print('WAF %s was not detected on %s' % (options.test, target))
        #     else:
        #         print(
        #             'WAF %s was not found in our list\r\nUse the --list option to see what is available' % options.test)
        #     return
        # 是否检测所有waf，这里只检测一个
        waf = attacker.identwaf()
        if len(waf) > 0:
            return 'The site %s is behind a %s' % (target, ' and/or '.join(waf))
        else:
            return 'No Waf detected'
        # if (options.findall) or len(waf) == 0:
        #     print('Generic Detection results:')
        #     if attacker.genericdetect():
        #         log.info('Generic Detection: %s' % attacker.knowledge['generic']['reason'])
        #         print('The site %s seems to be behind a WAF or some sort of security solution' % target)
        #         print('Reason: %s' % attacker.knowledge['generic']['reason'])
        #     else:
        #         print('No WAF detected by the generic detection')
        # print('Number of requests: %s' % attacker.requestnumber)
        
        
if __name__ == '__main__':
    print WafDetect().run(target='http://baidu.com/', headers={})




