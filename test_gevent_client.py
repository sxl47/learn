#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_gevent_client.py
@time: 2018/3/28 11:17
@desc:

"""
import socket
import traceback

import gevent
from gevent import monkey

monkey.patch_socket()


def reader(s):
    while True:
        try:
            data = s.recv(1024)
            print(u'接收到：{0}'.format(data))

            # cmd = input('input:')
            # cmd = "hello!!"  # 与人交互，输入命令
            # cmd = bytes(cmd, 'utf-8')
            # w = gevent.spawn(writer, s, cmd)
        except Exception as e:
            # s.close()
            print(e)
            # traceback.print_exc(e)
            break


def writer(s, msg):
    while True:
        try:
            s.sendall(msg)  # 把命令发送给对端
        except Exception as e:
            # s.close()
            print(e)
            # traceback.print_exc(e)
            break
        gevent.sleep(20)


def b():
    host = '192.168.0.196'
    # host = '122.114.126.123'
    # host = '192.168.11.101'
    port = 8082
    # print('connect-{0}:{1}:begin'.format(host, port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP

    # 在客户端开启心跳维护
    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.ioctl(socket.SIO_KEEPALIVE_VALS, (1, 1000*10, 1000*10))

    s.connect((host, port))  # 要连接的IP与端口
    # print('connect-{0}:{1}:end'.format(host, port))

    r = gevent.spawn(reader, s)
    w = gevent.spawn(writer, s, b"hello!")
    gevent.joinall([r, w])
    s.close()


def start():
    print('start^^^')
    tasks = []
    for i in range(1):
        task = gevent.spawn(b)
        tasks.append(task)
        if i != 0 and i % 100 == 0:
            print('start100')
            gevent.sleep(1)
    gevent.joinall(tasks)
    print('end^^^')


if __name__ == '__main__':
    start()
