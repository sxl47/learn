#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_socket.py
@time: 2018/3/27 14:28
@desc:

"""

import gevent
from gevent import socket


def recv(client):
    while True:
        try:
            data = client.recv(1024)
            print(u'接收到：{0}'.format(data))
        except Exception as e:
            print(e)


def send(client):
    while True:
        try:
            # gevent.sleep(1)
            # data = input('input:')
            data = b'broadcast'
            len = client.send(data)
            print(u'发送：{0}'.format(data))
            gevent.sleep(10)
        except Exception as e:
            print(e)


def client_start():
    # host = '192.168.0.196'
    host = '122.114.126.123'
    port = 8082
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义socket类型，网络通信，TCP
    client.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
    print(u'连接中……')
    client.connect((host, port))  # 要连接的IP与端口
    print(u'已连接……')

    gevent.joinall([
        gevent.spawn(send, client),
        gevent.spawn(recv, client),
    ])


def start():
    ts = []
    for i in range(1000):
        t = gevent.spawn(client_start)
        ts.append(t)

    gevent.joinall(ts)


if __name__ == '__main__':
    start()
