#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: asgi.py
@time: 2018/12/31 14:49:06
@desc:

"""

import os
import django
from channels.routing import get_default_application

# 这里填的是你的配置文件settings.py的位置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()
application = get_default_application()
