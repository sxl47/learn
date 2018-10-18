import os
import platform

from multiprocessing import cpu_count, Process

import gevent
from gevent import socket, monkey
import traceback
from multiprocessing import Process

# monkey.patch_os()
monkey.patch_all()

conns = {}


def accept(s):
    while True:
        try:
            conn, addr = s.accept()
            conns[conn] = addr
            gevent.spawn(read, conn)
        except Exception as e:
            print(e)


def read(conn):
    try:
        while True:
            data = conn.recv(1024)
            print('current process id:{0}'.format(os.getpid()))
            if not data:
                break
            else:
                gevent.spawn(write, conn, data)
    except Exception as e:
        traceback.print_exc(e)
    finally:
        conn.close()
        del conns[conn]


def write(conn, data):
    try:
        conn.send(data)
    except Exception as e:
        print(e)


def server_start():
    port = 8082
    s = socket.socket()
    if is_linux():
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.bind(('0.0.0.0', port))
    s.listen(500)

    gevent.joinall([
        gevent.spawn(accept, s),
    ])


def is_linux():
    return platform.system() == 'Linux'


def is_windows():
    return platform.system() == 'Windows'


def start():
    print('system:', platform.system())
    if is_linux():
        count = cpu_count()
        for i in range(count):
            p = Process(target=server_start)
            p.start()
    else:
        server_start()


if __name__ == '__main__':
    start()
    pass
