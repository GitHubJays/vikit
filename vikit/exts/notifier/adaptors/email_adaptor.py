#!/usr/bin/env python
# coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 06/24/17
"""

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import types

from vikit.core.basic import result

from . import adatporbase

########################################################################
class EmailAdaptor(adatporbase.AdaptorBase):
    """"""

    # ----------------------------------------------------------------------
    def __init__(self, config):
        """Constructor"""
        assert isinstance(config, dict)
        self._config = config

    @property
    def config(self):
        """"""
        return self._config

    def send(self, result):
        """"""
        try:
            smtp_obj = smtplib.SMTP_SSL(self.config['smtp_host'])
            smtp_obj.set_debuglevel(1)
            smtp_obj.login(self.config['user'], self.config['password'])

            msg = MIMEText(result, "plain", 'utf-8')
            msg["Subject"] = Header(self.config['title'], 'utf-8')
            msg["From"] = self.config['user']
            msg["To"] = self.config['send_to']
            smtp_obj.sendmail(self.config['user'], self.config['send_to'], msg.as_string())
            print("result send sucessfully")

        except smtplib.SMTPException:
            print("smtp config error")
