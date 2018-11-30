#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: pyqt_test.py
@time: 2017/12/2 15:42
@desc:

"""
import sys
from PyQt4 import QtCore
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QApplication, QCheckBox
from PyQt4.QtScript import *


class JsEngine(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.engine = QScriptEngine()
        t = self.engine.newQObject(self)
        self.engine.globalObject().setProperty("app", t)

    @QtCore.pyqtSlot(str)
    def exec_js(self, js):
        self.engine.evaluate(js)

        if self.engine.hasUncaughtException():
            line_num = self.engine.uncaughtExceptionLineNumber()
            sl = self.engine.uncaughtException().toString()
            print("line:{0},error:{1}".format(line_num, sl))

    @QtCore.pyqtSlot()
    def exec_js1(self):
        js = """
            var c = 123;
            """
        self.exec_js(js)

    @QtCore.pyqtSlot(str, str)
    def log(self, p1, p2):
        print
        p1, p2


def script_engine_test():
    app = QApplication(sys.argv)

    # 创建js引擎
    engine = QScriptEngine()

    fun = engine.evaluate("(function(a, b) { return a + b; })")
    args = [
        QScriptValue(1),
        QScriptValue(3)
    ]
    three_again = fun.call(QScriptValue(), args)
    print
    three_again.toInt32()

    # 创建qt对象到js引擎，js可调用这个实例对象
    button1 = QCheckBox('test---1')
    button2 = QCheckBox('test---2')
    button3 = QCheckBox('test---3')
    script_button1 = engine.newQObject(button1)
    script_button2 = engine.newQObject(button2)
    script_button3 = engine.newQObject(button3)
    engine.globalObject().setProperty("button1", script_button1)
    engine.globalObject().setProperty("button2", script_button2)
    engine.globalObject().setProperty("button3", script_button3)

    # 三种方式调用

    # 1、用js的方式调用
    engine.evaluate("button1.show()")
    engine.evaluate("button1.setChecked(true)")
    engine.evaluate("button1.setEnabled(false)")

    # 2、用js对象的方式调用
    script_button2.property("show").call()
    script_button2.property("setChecked").call(QScriptValue(), [QScriptValue(True)])
    script_button2.property("setEnabled").call(QScriptValue(), [QScriptValue(False)])

    # 3、用qt对象的方式调用
    button3.show()
    button3.setChecked(True)
    button3.setEnabled(False)

    sys.exit(app.exec_())


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
