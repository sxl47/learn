#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: start.py
@time: 2019/1/4 15:44:14
@desc:

"""

import sys

from PySide2.QtCore import QObject, Slot
from PySide2.QtWidgets import QApplication, QLabel
from PySide2.QtQml import QJSEngine


class JsEngine(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.engine = QJSEngine()
        t = self.engine.newQObject(self)
        self.engine.globalObject().setProperty("app", t)

    @Slot(str)
    def exec_js(self, js):
        val = self.engine.evaluate(js)
        # print("val:{0}".format(val.toString()))

    @Slot()
    def exec_js1(self):
        js = """
            var c = 123;
            """
        self.exec_js(js)

    @Slot(str, str)
    def log(self, p1, p2):
        print(p1, p2)


def js_recursion_call():
    # app = QApplication(sys.argv)
    tt = JsEngine()
    # 执行js
    js = """
    function main() {
        var a = 120;
        var b = 1;
        app.log(a,"tt1");
        app.log(b, "tt2");
        app.exec_js1();
        app.log(c, "tt3");
    };
    """
    r = tt.exec_js(js)
    r = tt.exec_js("main();")

    # sys.exit(app.exec_())


def start():
    app = QApplication(sys.argv)
    label = QLabel("Hello World")

    js_recursion_call()

    label.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
