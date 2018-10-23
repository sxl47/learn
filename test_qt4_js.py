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


def func():
    app = QApplication(sys.argv)

    # qt widget test
    # a = QWidget()
    # a.show()

    # 创建js引擎
    engine = QScriptEngine()

    fun = engine.evaluate("(function(a, b) { return a + b; })")
    args = [
        QScriptValue(1),
        QScriptValue(3)
    ]
    three_again = fun.call(QScriptValue(), args)
    print three_again.toInt32()

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


def test():
    class T(QObject):
        def __init__(self):
            QObject.__init__(self)

        @QtCore.pyqtSlot(str, str)
        def log(self, p1, p2):
            print p1, p2

    app = QApplication(sys.argv)
    engine = QScriptEngine()
    tt = T()
    t = engine.newQObject(tt)
    engine.globalObject().setProperty("app", t)
    # 执行js
    js = """
    function main() {
        var a = 120;
        var b = 1;
        app.log(1,"tt1");
        app.log(2, "tt2");
    } 
        """
    r = engine.evaluate(js)
    r = engine.evaluate("main();")

    if engine.hasUncaughtException():
        print(engine.uncaughtExceptionLineNumber())
        sl = engine.uncaughtException().toString()
        print(sl)
    sys.exit(app.exec_())


if __name__ == '__main__':
    test()
