#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: context_processors.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/9/20 10:16
# @description： django的上下文处理器

import logging

logger = logging.Logger(__name__)

# todo:创建blog之后改写
def seo_processor(request):
    value = {
        'SITE_NAME': 'my_blog',
        'SITE_DESCRIPTION': 'my_blog copy',
    }

    return value