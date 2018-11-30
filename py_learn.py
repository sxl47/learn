#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test.py
@time: 2018/11/29 23:00:52
@desc:

"""
from functools import reduce


def test1():
    """
    列表
    :return:
    """
    a_lst = [1, 2, 3, 4, 5]
    b_lst = [11, 22, 33, 44, 55, 66]
    print(a_lst)
    print(a_lst[1::2])

    r = zip(a_lst, a_lst[1::2])
    print(dict(r))
    print(*r)
    print(dict(zip(a_lst, b_lst)))

    print(reduce(lambda x, y: x + y, a_lst[1::2]))


def test2():
    class T(object):
        cls_val = 1

        def __init__(self):
            self.ins_val = 2

    t = T()
    print(T.__dict__)
    print(t.__dict__)
    T.cls_val = 22
    t.cls_val = 11
    print(T.__dict__)
    print(t.__dict__)


def start():
    test2()


if __name__ == '__main__':
    start()
