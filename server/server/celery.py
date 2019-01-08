#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: celery.py
@time: 2018/12/30 17:10:02
@desc:

"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from server import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')  # 设置django环境

app = Celery('server')

app.config_from_object('django.conf:settings')  # 使用CELERY_ 作为前缀，在settings中写配置

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
