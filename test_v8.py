#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_v8.py
@time: 2018/2/12 18:31
@desc:

"""
import traceback

from PyV8 import JSContext


def add(a, b):
    return a + b


class JsInterface(object):

    def __init__(self):
        pass

    def log(self, log_str, lvl):
        print log_str


def start():

    js = u'''
function f_and(a, b){
    return a+b;
}

app.log(add(4,7), 1);
// a = a
a = 1;
app.log(a, 0);
'''
    with JSContext() as ctx:
        try:
            js_interface = JsInterface()
            ctx.locals.add = add
            ctx.locals.app = js_interface
            ctx.eval(js)
            print ctx.locals.f_and(1, 8)
        except Exception, e:
            traceback.print_exc(e)


if __name__ == '__main__':
    start()
