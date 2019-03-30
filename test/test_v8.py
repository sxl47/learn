#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_v8.py
@time: 2018/2/12 18:31
@desc:

"""
import time
import traceback
import threading

from PyV8 import *
from PyV8 import JSIsolate


def add(a, b):
    return a + b


class JsInterface(object):

    def __init__(self):
        self.a = None

    def log(self, log_str, lvl):
        print(log_str)

    def sleep(self, n):
        time.sleep(n)

    def set_a(self, a):
        self.a = a

    def get_a(self):
        return self.a


class V8Thread(threading.Thread):

    def __init__(self):
        super(V8Thread, self).__init__()
        pass

    def run(self):
        js = u'''
    function f_and(a, b){
        app.log(a+'+'+b+'is:'+a+b, 0);
        return a+b;
    }
    
    app.log(add(4,7), 1);
    // a = a
    // app.sleep(3);
    a = 1;
    app.log(a, 0);
    '''
        with JSIsolate() as isolate:
            # with JSLocker(isolate):
            with JSContext() as ctx:
                with JSEngine() as engine:
                    try:
                        js_interface = JsInterface()
                        ctx.locals.add = add
                        ctx.locals.app = js_interface
                        # ctx.eval(js)
                        jsscipt = engine.compile(js)
                        jsscipt.run()
                        # ctx.locals.f_and(n, 8)
                        # print('add is {0}'.format(aa))
                    except Exception as e:
                        traceback.print_exc(e)


# import time, threading
#
#
# class Global:
#     result = []
#
#     def add(self, value):
#         # we use preemption scheduler to switch between threads
#         # so, just comment the JSUnlocker
#         #
#         # with JSUnlocker() as unlocker:
#         time.sleep(0.1)
#
#         self.result.append(value)
#
#
# def run():
#     g = Global()
#     with JSIsolate(True):
#         with JSContext(g) as ctxt:
#             ctxt.eval("""
#                 for (i=0; i<10; i++)
#                     add(i);
#             """)
#
#
# threads = [
#     threading.Thread(target=run),
#     threading.Thread(target=run)
# ]
#
# for t in threads: t.start()
# for t in threads: t.join()

if __name__ == '__main__':
    pass

    threads = []
    for i in range(2):
        t = V8Thread()
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
