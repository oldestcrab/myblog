#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: utils.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/19 14:44
# @description： 一些通用函数

import logging
from hashlib import md5
from django.contrib.sites.models import Site
from django.conf import settings

logger = logging.getLogger(__name__)

def get_md5(str):
    """对字符串进行md5加密

    :param str: 字符串
    :return: 加密后的字符串md5值
    """
    m = md5(str.encode('utf-8'))
    return m.hexdigest()

def send_email(emailto, title, content):
    from my_blog.blog_signals import  send_email_signal
    send_email_signal.send(send_email.__class__, emailto=emailto, title=title, content=content)

# TODO: 为视图增加缓存
def get_current_site():
    site = Site.objects.get_current()
    return site

# TODO: 为设置增加缓存，创建blog之后改写
def get_blog_setting():
    value = {

    }

if __name__ == '__main__':
    print(get_md5('好的'))
