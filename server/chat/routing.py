#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: routing.py
@time: 2018/12/31 14:45:00
@desc:

"""

from django.conf.urls import url

from chat import consumer

websocket_urlpatterns = [
    # consumers.DeployResult 是该路由的消费者
    # url(r'^ws/deploy/(?P<service_name>[^/]+)/$', consumer.DeployResult),
    url(r'^ws/chat/(?P<group>[^/]+)/(?P<uid>[^/]+)$', consumer.DeployResult),
]
