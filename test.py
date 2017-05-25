#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Test for vikit
  Created: 05/16/17
"""

from __future__ import unicode_literals

import unittest
import time

from vikit.core.target import Target, TargetEnum, \
     TYPE_IPV4, TYPE_IPV6, TYPE_NETLOC, \
     TYPE_URL, TYPE_RAW, TYPE_AUTO, TYPE_FILE

from vikit.core.payload import Payload, PayloadEnum, TYPE_TEXT, TYPE_FILE
from vikit.core.mixer import mixer
from vikit.core.param import Param, \
     TYPE_JSON, \
     TYPE_INT, TYPE_STR, TYPE_BOOL, TYPE_FLOAT, \
     TYPE_ENUM, TYPE_BYTES, \
     ParamSet

from vikit.core.modinput import ModInput, TargetDemand, PayloadDemand, ParamDemand
from vikit.core.mod import ModBasic, ModStandard, ModFactory

from vikit.dbm import kvpersist
from vikit.core import result
from vikit.core import utils
from vikit.core import modmanager
from vikit.core import service
from vikit.core.service import serializer


class Test(object):
    #----------------------------------------------------------------------
    def __init__(self):
        """"""
        self._ini = 'asdfa'
        self._bse = 'asdf' 


########################################################################
class VikitTester(unittest.TestCase):
    """"""

    #----------------------------------------------------------------------
    def test_core(self):
        """"""
        #
        # test target/targets
        #
        _target = Target(target='45.78.6.64', type=TYPE_AUTO)
        self.assertEqual(_target.type, TYPE_IPV4)
        
        _targets = TargetEnum(targets=['45.78.6.64', '54.34.23.6'], type=TYPE_IPV4)
        _targets = TargetEnum(targets=['45.78.6.64:34', '54.34.23.6:76'], type=TYPE_IPV4)
        _targets = TargetEnum(targets=['tbis.me:23', 'sss.com:80'], type=TYPE_NETLOC)
        _targets = TargetEnum(targets=['http://tbis.me:23', 'http://sss.com:80'], type=TYPE_URL)
        _targets1 = TargetEnum(targets=['README.md'], type=TYPE_FILE)
        _targets1 = TargetEnum(name='target1', targets=['README.md'], type=TYPE_FILE)
        
        assert _targets.name == 'target'
        assert _targets1.name == 'target1'
        
        #
        # test payload/payloads
        #
        _pl = Payload('asdfasdf', TYPE_TEXT)
        _pl = Payload('safsadf', TYPE_TEXT)
        _pl = Payload('README.md', TYPE_TEXT, name='payload_test_name')
        _pls = PayloadEnum(['README.md', 'test.py'], TYPE_TEXT)

        assert _pl.name == 'payload_test_name'
        assert _pls.name == 'payload'

        #
        # target/payload mix 
        #
        count = 0
        for i in mixer(_pl, _targets):
            count = count + 1
        self.assertEqual(count, 2)        
        
        count = 0
        for i in mixer(_pls, _targets):
            count = count + 1
        self.assertEqual(count, 4)

        b = Param(name='arg4', value='"json"', type=TYPE_JSON)
        Param(name='arg1', value='json', type=TYPE_STR)
        c = Param(name='arg3', have_to=False, value=None, type=TYPE_INT)
        Param(name='arg1', value=3, type=TYPE_FLOAT)
        d = Param(name='arg2', value=None, type=TYPE_FLOAT)
        Param(name='arg1', value=True, type=TYPE_BOOL)
        Param(name='arg1', value=b'\xff\xff\xff\xff', type=TYPE_BYTES)
        
        s = Param(name='arg1', value=[1,2,3,4], type=TYPE_ENUM)
        
        _ = s.check()
        self.assertTrue(_)
        
        _ = c.check()
        self.assertTrue(_)
        
        _ = d.check()
        self.assertFalse(_)
        d.value = '12.3'
        self.assertTrue(d.check())
        
        self.assertEqual(s.name, 'arg1')
    
        paramset_obj = ParamSet(s, b, c, d)
        
        _ = paramset_obj.get('arg1')
        assert _ == [1,2,3,4]
        _ = paramset_obj.get_param('arg1')
        assert isinstance(_, Param)
        _ = paramset_obj.get_param_obj_by_name('arg1')
        assert isinstance(_, Param)
        print('*' * 64)
        print( paramset_obj.dumped())
        print( paramset_obj.get_params())
        print( paramset_obj.now())
        print( '*' * 64)
        print( paramset_obj.set('arg1', [5,6,7,8]))
        self.assertEqual(paramset_obj.get('arg1'), [5,6,7,8])
        
        self.assertFalse(paramset_obj.has_key('asfdasdf'))
        self.assertTrue(paramset_obj.has_key('arg1'))
        self.assertTrue(paramset_obj.has_key('arg2'))
        self.assertTrue(paramset_obj.has_key('arg3'))
        self.assertTrue(paramset_obj.has_key('arg4'))
        
        s.value = None
        _r, unset = paramset_obj.check()
        self.assertFalse(_r)
        self.assertEqual(len(unset), 1)
        
        demand1 = TargetDemand(dst='target', dst_type=TYPE_RAW)
        demand2 = PayloadDemand(dst='payload1', dst_type=TYPE_FILE)
        demand3 = PayloadDemand(dst='payload2')
        demand4 = ParamDemand(dst='p1', dst_type=TYPE_STR)
        
        modinput = ModInput(demand1, demand2, demand3, demand4)
        _, unset = modinput.check()
        assert not _
        assert len(unset) == 4
        
        target = TargetEnum(targets=['1,23,4', 'adfasdfasd'], type=TYPE_RAW)
        payload1 = Payload(payload='README.md', type=TYPE_FILE, name='payload1')
        payload2 = PayloadEnum(payloads=list('README.md'), type=TYPE_TEXT, name='payload2')
        param1 = Param(name='p1', value='test')
        modinput.match(target, param1, payload1, payload2)
        
        pset = modinput.paramset
        ts = modinput.targets
        tss = modinput.payloads
        
        for i in modinput:
            print i
    
        #
        # mod test
        #
        
        def testfunc(target, payload1, payload2, config):
            time.sleep(3)
            print('execute: {},{}:{} config:{}'.\
                  format(target, payload1, payload2, config))
            return 'execute success!'
        
        mod = ModBasic(name='test')
        #mod.from_module(filename='')
        mod.from_function(func=testfunc)
        modinput.reset()
        
        _count = 0
        for i in modinput:
            _count = _count + 1
            modinput.check_from_dict(i)
            mod.execute(i)
        
        result_q = mod.result_queue
    
        #mod.join()
        
        queue_ = mod.result_queue
        
        print('got queue')
        queue_.get()
        queue_.get()
        queue_.get()
        queue_.get()
        
        
        def testerror(target):
            raise StandardError('adfa')
        
        mod = ModBasic(name='ss')
        mod.from_function(testerror)
        mod.execute({'target':'adfasdf'})
    
    #----------------------------------------------------------------------
    def test_dbm(self):
        """"""
        kvm = kvpersist.KVPersister('./vikit/datas/test.db')
        kvm.set(key='testkey', value='testvalues')
        assert 'testvalues' == kvm.get(key='testkey')
        assert None == kvm.get(key='testkey1')
        self.assertTrue(kvm.has_key(key='testkey'))
        self.assertFalse(kvm.has_key(key='testkey1'))
        self.assertFalse(kvm.delete(key='testkey1'))
        self.assertTrue(kvm.delete(key='testkey'))
        kvm.close()
    
    #----------------------------------------------------------------------
    def test_result(self):
        """"""
        result_demo = {'state':True,
                       'result':{'config':'adfasdf',
                                 'from':'45.78.6.64'},
                       'targets':{'1':'https://villanch.top',
                                  '2':'http://asdfasdf.com'}}
        
        _r = result.Result(result_demo)
        targets = _r.extract_targets()
        assert len(targets) > 0
        def tar(x):
            print(x)
            assert isinstance(x, Target)
        
        map(tar, targets)
    
    #----------------------------------------------------------------------
    def test_got_standard_mod(self):
        """"""
        mods = ModStandard(name='testmod')
        
        module_demo = __import__('demo')
        mods.from_module(module_obj=module_demo)
        
        mods.execute({'target':'http://villanch.top',
                      'payload':'adfasdfasdf',
                      'config':{'param1':True,
                                'param2':'asdfasdf'}})
        time.sleep(5)
        _queue = mods.result_queue
        #self.assertEqual(_queue.qsize(), 1)
        print()
        print()
        print()
        
        print('WAITING FOR STANDARD MOD RESULT')
        print()
        print()
        print()
        
        _r = _queue.get()
        assert isinstance(_r, result.Result)
        
        targets = _r.extract_targets()
        assert len(targets) > 0
        def tar(x):
            print(x)
            assert isinstance(x, Target)
        
        map(tar, targets)
        
        mods.close()
    
    
    #----------------------------------------------------------------------
    def test_serialize(self):
        """"""
        s = serializer.Serializer()

            
        text = s.serialize(Test())
        text = s.unserialize(text)
        self.assertIsInstance(text, Test)
    
        
            
        
    #----------------------------------------------------------------------
    def test_modfactory(self):
        """"""
        _factory = ModFactory(min_threads=5, max_threads=20, debug=True,
                              loop_interval=0.2, adjust_interval=3, diviation_ms=100)
        
        
        _demo = __import__('demo')
        standardmod = _factory.build_standard_mod_from_module(_demo, min_thread=1)
        assert isinstance(standardmod, ModStandard)
        
        standardmod.execute(modinput_dict={"target":'http://tbis.me',
                                           'payload':'adfa',
                                           'config':{'param1':True,
                                                     'param2':'asdfasd'}})
        _q = standardmod.result_queue
        #print('WAITING A RESULT!')
        print()
        print()
        print()
        print()
        print('WAITING FOR STANDARD MOD RESULT')
        print()
        print()
        print()
        print()
        
        _r = _q.get()
        assert isinstance(_r, result.Result)
    
    
    

        
        
if __name__ == '__main__':
    unittest.main()