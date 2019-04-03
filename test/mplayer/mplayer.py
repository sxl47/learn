#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_mplayer.py
@time: 2019/4/3 17:23:13
@desc:

"""
import os
import sys

from PyQt4.QtCore import QProcess, QStringList, QTimer, QString
from PyQt4.QtGui import QApplication, QWidget

import mplayer_ui


class Player(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = None
        self.process = None
        self.init_ui()

    def init_ui(self):
        self.ui = mplayer_ui.Ui_mplayer()
        self.ui.setupUi(self)

        # 播放器初始化
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_player_stdout)
        time_clock = QTimer(self)
        time_clock.timeout.connect(self.time_done)

        # 播放视频
        path = '1.mp4'
        self.play_video(path)

    def time_done(self):
        self.process.write("get_time_length\n")
        self.process.write("get_time_pos\n")
        self.process.write("get_percent_pos\n")

    def read_player_stdout(self):

        while self.process.canReadLine():
            b = self.process.readLine()
            print(b)

            if b.startsWith("ANS_TIME_POSITION"):
                print(b)
            elif b.startsWith("ANS_LENGTH"):
                print(b)
            elif b.startsWith("ANS_PERCENT_POSITION"):
                print(b)

    def play_video(self, path):
        if not os.path.exists(path):
            print('not exists:{0}'.format(path))
            return
        args = QStringList()
        args << "-slave"  # 使用slave模式
        # args << "-quiet"  # 不要输出冗余信息
        args << "-wid" << QString.number(self.winId(), 10)  # 将输出定位到ui下的widget窗口内
        args << "-zoom"  # 自适应窗口
        args << "-vo"
        args << "x11,xv,gl,gl2,sdl"  # 使用x11模式播放(只有这种模式下才支持23行的指定输出窗口到ui->widget)
        args << path  # 播放file_name文件
        self.process.start("MPlayer/mplayer.exe", args)  # 启动该进程，并传入参数args


def start():
    app = QApplication(sys.argv)
    player = Player()
    player.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()
