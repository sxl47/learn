#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: routing.py
@time: 2018/12/31 14:54:48
@desc:

"""

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns  # 指明路由文件是chat/routing.py
        )
    ),
})
