#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: tasks.py
@time: 2018/12/30 17:45:54
@desc:

"""

from __future__ import absolute_import
from celery import shared_task
import time


@shared_task(track_started=True)
def add(x, y):
    # time.sleep(30)  # 模拟长时间执行
    return x + y


def start():
    pass


if __name__ == '__main__':
    start()
