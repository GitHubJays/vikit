#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2016/12/1
"""

import unittest

from dns import query
from dns import zone
from dns import resolver
from dns import rdataclass, rdatatype
from pprint import pprint
from dns.exception import FormError
from pprint import pprint

NONE = 0
A = 1
NS = 2
MD = 3
MF = 4
CNAME = 5
SOA = 6
MB = 7
MG = 8
MR = 9
NULL = 10
WKS = 11
PTR = 12
HINFO = 13
MINFO = 14
MX = 15
TXT = 16
RP = 17
AFSDB = 18
X25 = 19
ISDN = 20
RT = 21
NSAP = 22
NSAP_PTR = 23
SIG = 24
KEY = 25
PX = 26
GPOS = 27
AAAA = 28
LOC = 29
NXT = 30
SRV = 33
NAPTR = 35
KX = 36
CERT = 37
A6 = 38
DNAME = 39
OPT = 41
APL = 42
DS = 43
SSHFP = 44
IPSECKEY = 45
RRSIG = 46
NSEC = 47
DNSKEY = 48
DHCID = 49
NSEC3 = 50
NSEC3PARAM = 51
TLSA = 52
HIP = 55
CDS = 59
CDNSKEY = 60
CSYNC = 62
SPF = 99
UNSPEC = 103
EUI48 = 108
EUI64 = 109
TKEY = 249
TSIG = 250
IXFR = 251
AXFR = 252
MAILB = 253
MAILA = 254
ANY = 255
URI = 256
CAA = 257
AVC = 258
TA = 32768
DLV = 32769

rdatatype_dict = {
    'NONE': NONE,
    'A': A,
    'NS': NS,
    'MD': MD,
    'MF': MF,
    'CNAME': CNAME,
    'SOA': SOA,
    'MB': MB,
    'MG': MG,
    'MR': MR,
    'NULL': NULL,
    'WKS': WKS,
    'PTR': PTR,
    'HINFO': HINFO,
    'MINFO': MINFO,
    'MX': MX,
    'TXT': TXT,
    'RP': RP,
    'AFSDB': AFSDB,
    'X25': X25,
    'ISDN': ISDN,
    'RT': RT,
    'NSAP': NSAP,
    'NSAP-PTR': NSAP_PTR,
    'SIG': SIG,
    'KEY': KEY,
    'PX': PX,
    'GPOS': GPOS,
    'AAAA': AAAA,
    'LOC': LOC,
    'NXT': NXT,
    'SRV': SRV,
    'NAPTR': NAPTR,
    'KX': KX,
    'CERT': CERT,
    'A6': A6,
    'DNAME': DNAME,
    'OPT': OPT,
    'APL': APL,
    'DS': DS,
    'SSHFP': SSHFP,
    'IPSECKEY': IPSECKEY,
    'RRSIG': RRSIG,
    'NSEC': NSEC,
    'DNSKEY': DNSKEY,
    'DHCID': DHCID,
    'NSEC3': NSEC3,
    'NSEC3PARAM': NSEC3PARAM,
    'TLSA': TLSA,
    'HIP': HIP,
    'CDS': CDS,
    'CDNSKEY': CDNSKEY,
    'CSYNC': CSYNC,
    'SPF': SPF,
    'UNSPEC': UNSPEC,
    'EUI48': EUI48,
    'EUI64': EUI64,
    'TKEY': TKEY,
    'TSIG': TSIG,
    'IXFR': IXFR,
    'AXFR': AXFR,
    'MAILB': MAILB,
    'MAILA': MAILA,
    'ANY': ANY,
    'URI': URI,
    'CAA': CAA,
    'AVC': AVC,
    'TA': TA,
    'DLV': DLV,
}

quick_type = {
    'A':A,
    "A":AAAA,
    'NS':NS,
    'MX':MX,
    'SOA':SOA,
    'TXT':TXT,
    'CNAME':CNAME
}


#----------------------------------------------------------------------
def dns_query_quick(target_domain):
    """"""
    #global rdatatype
    
    START_BANNER = ';ANSWER'
    END_BANNER = ';AUTHORITY'
    
    result = {}
    for i in quick_type.items():
        try:    
            #print '-------------------------------------'
            
            r = resolver.query(target_domain, i[1])
            #print '-------------------------------------'
            #print i[0]  
            result_list = r.response.to_text().splitlines()
            content = result_list[result_list.index(START_BANNER)+1:\
                                  result_list.index(END_BANNER)]
            #print content
            result[i[0]] = content
            #print '-------------------------------------'
        except:
            
            pass
            #print '[!] No Sucn Anwser'
            
    #print zone.from_text(r)
    #pprint(result)
    return result    

#----------------------------------------------------------------------------
def dns_query_all(target_domain):
    """"""
    global rdatatype
    
    START_BANNER = ';ANSWER'
    END_BANNER = ';AUTHORITY'
    
    result = {}
    for i in rdatatype_dict.items():
        try:    
            #print '-------------------------------------'
            
            r = resolver.query(target_domain, i[1])
            #print '-------------------------------------'
            #print i[0]  
            result_list = r.response.to_text().splitlines()
            content = result_list[result_list.index(START_BANNER)+1:\
                                  result_list.index(END_BANNER)]
            #print content
            result[i[0]] = content
            #print '-------------------------------------'
        except:
            
            pass
            #print '[!] No Sucn Anwser'
            
    #print zone.from_text(r)
    #pprint(result)
    return result

#r = query.xfr(where='dns2.sdp.edu.cn', zone='sdp.edu.cn')


#----------------------------------------------------------------------
def dns_zone_transfer_check(target, ns_server):
    """"""
    assert isinstance(target, (unicode, str))
    
    result = ''
    
    r = query.xfr(where=ns_server, zone=target)
    try:
        _ = zone.from_xfr(r).to_text()
        result = _
    except FormError:
        pass
    
    return result
#----------------------------------------------------------------------
def get_ns_server(target):
    """"""
    assert isinstance(target, (str, unicode))
    ns_list_buffer = []
    _dns_result = dns_query_all(target)
    try:
        ns_list = _dns_result['NS']
    except AttributeError:
        return ns_list_buffer
    
    for i in ns_list:
        _ns_s = i.split()[-1]
        if _ns_s.endswith('.'):
            _ns_s = _ns_s[:-1]
        ns_list_buffer.append(_ns_s)
    
    return ns_list_buffer

if __name__ == '__main__':
    print get_ns_server(target='uestc.edu.cn')
        