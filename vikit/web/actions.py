#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Actions
  Created: 07/02/17
"""

import json

from .app import client_app

from ..api.trigger import get_client_proxy

proxy = None

@client_app.route('/start')
def start():
    """"""
    global proxy
    
    proxy = get_client_proxy('127.0.0.1', 7000)
    return '<h1>Success</h1>'



@client_app.route('/shutdown')
def shutdown():
    """"""
    global proxy

    proxy.shutdown()
    return '<h1>Success</h1>'

@client_app.route('/available-modules')
def get_available_module():
    """"""
    global proxy
    proxy.get_available_modules()
    return json.dumps(proxy.get_available_modules())

@client_app.route('/execute/<module_name>')
def execute():
    """"""
    return ''

@client_app.route('/help/<module_name>')
def help(module_name):
    """"""
    global proxy
    _ret = proxy.get_help_for_module(module_name)
    return json.dumps(_ret)
    