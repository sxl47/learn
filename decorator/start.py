#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: start.py
@time: 2019/3/13 11:57:04
@desc:

"""


def enter(self):
    return self


def exit(self, exc_type, exc_val, exc_tb):
    pass


class A(object):

    def __init__(self):
        self.var_a = "231421342"


A.__enter__ = enter
A.__exit__ = exit


def get_a():
    return A()


def start():
    a = get_a()
    print(a.__dict__)

    with get_a() as a:
        pass


if __name__ == '__main__':
    start()
