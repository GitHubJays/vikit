#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/6/24 17:13
# @Author  : Conan
# @Function: feedback scan result by email,wechat and etc

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from vikit.core.basic import result


class Sender(object):
    def send(self, title, text, send_to):
        pass


class QQEmailSmtpSenderAdaptee(Sender):
    def __init__(self, smtp_host='smtp.qq.com', port=465, username='1526840124', password='uoqbqzlmhrswfjef'):
        self.smtp_host = smtp_host
        self.port = port
        self.username = username
        self.password = password
        self.username_mail = self.username + '@qq.com'

    def specific_send(self, title, text, send_to):
        try:
            smtp_obj = smtplib.SMTP_SSL(self.smtp_host)
            smtp_obj.set_debuglevel(1)
            smtp_obj.login(self.username, self.password)

            msg = MIMEText(text, "plain", 'utf-8')
            msg["Subject"] = Header(title, 'utf-8')
            msg["From"] = self.username_mail
            msg["To"] = send_to
            smtp_obj.sendmail(self.username_mail, send_to, msg.as_string())
            print("result send sucessfully")

        except smtplib.SMTPException:
            print("smtp config error")


class AdapterSender(Sender):
    def __init__(self, sender_adaptee):
        self.sender_adaptee = sender_adaptee

    def send(self, title, text, send_to):
        self.sender_adaptee.specific_send(title, text, send_to)


class ResultFeedback(object):
    def __init__(self, adapter_sender, scan_result, send_to):
        self.adapter_sender = adapter_sender
        self.scan_title = 'scan result'
        self.scan_result = str(scan_result)
        assert isinstance(scan_result, result.Result)
        self.send_to = send_to

    def feedback_result(self):
        self.adapter_sender.send(self.scan_title, self.scan_result, self.send_to)


if __name__ == "__main__":
    qq_email_adaptee = QQEmailSmtpSenderAdaptee()
    adapter_sender = AdapterSender(qq_email_adaptee)
    result_demo = {'state': True,
                   'result': {'config': 'adfasdf',
                              'from': '45.78.6.64'},
                   'targets': {'1': 'https://villanch.top',
                               '2': 'http://asdfasdf.com'}}
    result_feedback = ResultFeedback(adapter_sender, result.Result(result_demo), '1526840124@qq.com')
    result_feedback.feedback_result()
