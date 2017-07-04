#!/usr/bin/env python
# coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Define Actions
  Created: 07/02/17
"""

import json

from .app import client_app

from ..api.trigger import get_client_proxy

from flask import render_template, request, jsonify
from flask import session, redirect, url_for, make_response

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


@client_app.route('/help/<module_name>')
def help(module_name):
    """"""
    global proxy
    _ret = proxy.get_help_for_module(module_name)
    return json.dumps(_ret)


# common route
@client_app.route('/', methods=['GET'])
def main():
    """"""
    return render_template('main.html')


@client_app.route('/select_module/<module_name>', methods=['GET'])
def on_select_module(module_name):
    """
    return module_help and module params 
    """
    global proxy
    _ret = proxy.get_help_for_module(module_name)
    module_help = json.dumps(_ret)
    return render_template('main.html', module_help=module_help, selected_module=module_name)


@client_app.route('/execute/<module_name>', methods=['POST'])
def execute(module_name):
    """
    get params from form and translate into json then execute
    """
    # def execute(self, module_name, params, offline=False, task_id=None):
    global proxy
    target = request.form['target']
    payload = request.form['payload']
    config = json.loads(request.form['config'])
    task_id = request.form['task_id']
    offline = request.form['offline']
    params = {
        'target': target,
        'payload': payload,
        'config': config,
    }
    proxy.execute(module_name, params, offline=offline, task_id=task_id)
    redirect(url_for('/result/' + task_id))


@client_app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    '''return the task result according the task_id'''
    result = None
    return render_template('result.html', task_id=task_id, result=result)

