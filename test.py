#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test.py
@time: 2018/3/27 18:12
@desc:

"""
import time
from multiprocessing import Process


def task1(msg):
    print('task1: hello, %s' % msg)
    time.sleep(1)


def task2(msg):
    print('task2: hello, %s' % msg)
    time.sleep(1)


def task3(msg):
    print('task3: hello, %s' % msg)
    time.sleep(1)


if __name__ == '__main__':

    p1 = Process(target=task1, args=("111",))
    p1.start()

