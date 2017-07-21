#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test the host is alive?
  Created: 2016/12/20
"""

import unittest
import pexpect
#from ping import verbose_ping

#----------------------------------------------------------------------
def shping(target, timeout=2, count=4):
    """"""
    #if count > timeout:
    timeout = max([timeout, count]) + 1 
    result = pexpect.run('ping {target}'.format(target=target), timeout=timeout)
    lines = result.splitlines()
    
    _ret = {}
    
    for i in lines:
        for j in i.split():
            if '=' in j or u'=' in j:
                key = j.split('=')[0].strip()
                val = j.split('=')[1].strip()
                
                if val.isdigit():
                    if _ret.get(key):
                        _ret[key] = (_ret[key] + int(val)) / 2
                    else:
                        _ret[key] = int(val)
                else:
                    try:
                        if _ret.get(key):
                            _ret[key] = (_ret[key] + float(val)) / 2
                        else:
                            _ret[key] = float(val)
                    except:
                        pass
    
    #
    # Set delay
    #
    try:
        if _ret.get('delay'):
            pass
        else:
            _ret['delay'] = _ret.get('time')
    except:
        _ret['delay'] = None
    
    
    return _ret

#----------------------------------------------------------------------
def is_alive(host, timeout=2, count=4):
    """"""
    result = {}
    
    ret = ping_host(host, timeout, count)
    result[host] = ret
    
    return result


#----------------------------------------------------------------------
def ping_host(host, timeout=2, count=4):
    """"""
    result = {}
    result['alive'] = False
    result['delay'] = None
    try:
        result['delay'] = shping(host, timeout, count).get('delay')
        if result.get('delay'):
            result['alive'] = True
        else:
            pass
    except:
        pass
    
    return result


########################################################################
class IsAliveTest(unittest.case.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_pingtest(self):
        """Ping test"""
        
        print shping('villanch.top')
        
        
    
    

if __name__ == '__main__':
    unittest.main()