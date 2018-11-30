#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_qt_js.py
@time: 2018/10/23 15:38:54
@desc:

"""
import sys

from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtQml import QJSEngine


class JsEngine(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.engine = QJSEngine()
        t = self.engine.newQObject(self)
        self.engine.globalObject().setProperty("app", t)

    @pyqtSlot(str)
    def exec_js(self, js):
        val = self.engine.evaluate(js)
        if not val.isNull() and not val.isUndefined():
            print("error:{0}".format(val.toString()))

    @pyqtSlot()
    def exec_js1(self):
        js = """
            var c = 123;
            """
        self.exec_js(js)

    @pyqtSlot(str, str)
    def log(self, p1, p2):
        print(p1, p2)


def js_recursion_call():
    app = QApplication(sys.argv)
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

    sys.exit(app.exec_())


def start():
    js_recursion_call()


if __name__ == '__main__':
    start()
