#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_gevent_server.py
@time: 2018/3/27 19:46
@desc:

"""
import traceback

import gevent
import time

from gevent.queue import Queue
from gevent.server import StreamServer
from gevent.pywsgi import WSGIServer


class TClient(object):

    def __init__(self, sock, addr):
        self.name = None
        self.sock = sock
        self.addr = addr
        self.write_queue = Queue()

    def __str__(self):
        return '{0}:{1}'.format(self.addr[0], self.addr[1])

    def read(self):
        data = self.sock.recv(1024)
        return data

    def write(self, msg):
        self.sock.sendall(msg)

    def send(self, msg):
        self.write_queue.put(msg)

    def close(self):
        self.sock.close()
        self.send(b'__exit__')


class TServer(object):
    __TYPE_HIS_CLIENT = 100  # TYPE-历史客户端个数key

    def __init__(self):
        self.clients = {}
        self.dict_infos = {
            self.__TYPE_HIS_CLIENT: 0
        }

    def del_client(self, client, type):
        if client.sock in self.clients:
            print('{0}-{1} disconnected...'.format(client, type))
            client.close()
            del self.clients[client.sock]

    def broadcast(self, msg):
        for _, client in self.clients.items():
            client.send(msg)

    def reader(self, client):
        while True:
            try:
                data = client.read()
                if not data:
                    raise Exception('client disconnected')

                if data == b'broadcast':
                    self.broadcast(b'haha')

                msg = b"h"
                client.send(msg)

                # do others
                # print("get data from {0}-{1}".format(client, data))
                pass
            except Exception as e:
                print(e)
                self.del_client(client, 2)
                break

    def writer(self, client):
        while True:
            try:
                msg = client.write_queue.get()
                if msg == b'__exit__':
                    raise Exception('client exit')
                else:
                    client.write(msg)
            except Exception as e:
                print(e)
                self.del_client(client, 1)
                break

    def handle(self, sock, client_addr):

        t = int(time.time())

        self.dict_infos[self.__TYPE_HIS_CLIENT] += 1

        print('{0}:{1} connected...'.format(client_addr[0], client_addr[1]))

        client = TClient(sock, client_addr)
        self.clients[sock] = client

        try:
            r = gevent.spawn(self.reader, client)
            w = gevent.spawn(self.writer, client)
            gevent.joinall([r, w])
        finally:
            self.del_client(client, 0)

    def timer_log(self):
        while True:
            print('''
##########################################################
current connect:{0}
history connect:{1}
##########################################################
            '''.format(len(self.clients), self.dict_infos[self.__TYPE_HIS_CLIENT]))
            gevent.sleep(10)

    def http_request(self, env, start_response):
        # print('{0}:{1} connected...'.format(env['REMOTE_ADDR'], env['REMOTE_PORT']))
        start_response('200 OK', [('Content-Type', 'text/html')])
        gevent.sleep(0.1)
        return [b"<b>hello world</b>"]

    def start(self, ip, port):

        gevent.spawn(self.timer_log)

        print('server on {0}:{1}'.format(ip, port))
        s = StreamServer((ip, port), self.handle)
        s.serve_forever()

    def start_http_server(self, ip, port):
        s = WSGIServer((ip, port), self.http_request)
        s.serve_forever()

    def dispath_task(self, task_queue):
        while True:
            msg = task_queue.get()
            self.broadcast(msg)

    def do_task(self, task_queue):
        gevent.spawn(self.dispath_task, task_queue)


def gen_task(task_queue):
    i = 0
    while True:
        i += 1
        task = "test{0}^".format(i)
        task = bytes(task, 'utf-8')
        # task = task.decode('utf-8')
        task_queue.put(task)
        gevent.sleep(1)


def start():
    ip = '0.0.0.0'
    port = 8082

    task_queue = Queue()

    # gevent.spawn(gen_task, task_queue)

    server = TServer()
    server.do_task(task_queue)
    server.start(ip, port)
    # server.start_http_server(ip, port)


if __name__ == '__main__':
    start()
