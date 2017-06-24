#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/24 23:03
# @Author  : Conan
# @Function: notifier test

import sys

sys.path.append('..')

import unittest

from notifier import NotifyConfig, Notifier, EMAIL_ADAPTOR

from vikit.core.basic import result


class NotifierTest(unittest.TestCase):
    """"""

    def test_NotifyConfig(self):
        config = {'smtp_host': 'smtp.qq.com', 'user': '1526840124@qq.com', 'password': 'uoqbqzlmhrswfjef',
                  'send_to': '1526840124@qq.com', 'title': 'scan result test'}
        _NC = NotifyConfig()
        _NC.add_adaptor(EMAIL_ADAPTOR, config)
        self.assertEqual(_NC.adaptors[0].config['smtp_host'], 'smtp.qq.com')
        self.assertEqual(_NC.adaptors[0].config['user'], '1526840124@qq.com')
        self.assertEqual(_NC.adaptors[0].config['password'], 'uoqbqzlmhrswfjef')
        self.assertEqual(_NC.adaptors[0].config['send_to'], '1526840124@qq.com')
        self.assertEqual(_NC.adaptors[0].config['title'], 'scan result test')


    def test_Notifier(self):
        config = {'smtp_host': 'smtp.qq.com', 'user': '1526840124@qq.com', 'password': 'uoqbqzlmhrswfjef',
                  'send_to': '1526840124@qq.com', 'title': 'scan result test'}
        _NC = NotifyConfig()
        _NC.add_adaptor(EMAIL_ADAPTOR, config)
        notifier = Notifier(_NC)
        result_demo = {'state': True,
                       'result': {'config': 'adfasdf',
                                  'from': '45.78.6.64'},
                       'targets': {'1': 'https://villanch.top',
                                   '2': 'http://asdfasdf.com'}}
        # check email in your mail
        notifier.notify(result.Result(result_demo))


if __name__ == "__main__":
    unittest.main()
