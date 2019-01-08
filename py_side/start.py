#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: start.py
@time: 2019/1/4 15:44:14
@desc:

"""


def start():
    import sys
    from PySide2.QtWidgets import QApplication, QLabel

    app = QApplication(sys.argv)
    label = QLabel("Hello World")
    label.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
