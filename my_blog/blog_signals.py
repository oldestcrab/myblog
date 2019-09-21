#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: blog_signals.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/19 15:16
# @description： 

import logging
import django.dispatch
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.Logger(__name__)

send_email_signal = django.dispatch.Signal(providing_args=['emailto', 'title', 'content'])

@receiver(send_email_signal)
def send_email_signal_handler(sender, **kwargs):
    emailto = kwargs['emailto']
    title = kwargs['title']
    content = kwargs['content']

    msg = EmailMultiAlternatives(title, content, from_email=settings.DEFAULT_FROM_EMAIL, to= emailto)
    msg.content_subtype = 'html'
    # TODO: 管理员邮件发送日志之后增加
    try:
        result = msg.send()
    except Exception as e:
        logger.error(e)