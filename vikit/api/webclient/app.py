#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<v1ll4n>
  Purpose: Web API
  Created: 06/24/17
"""

from flask import Flask

CLIENT = None
app = Flask(__name__)


#----------------------------------------------------------------------
def set_client(client):
    """"""
    CLIENT = client

#----------------------------------------------------------------------
def run_web_service(port):
    """"""
    app.run(host='127.0.0.1', port=port, debug=True)
    

