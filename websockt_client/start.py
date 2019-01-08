#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: start.py
@time: 2018/12/31 10:51:50
@desc:

"""
import json

import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        while True:
            try:
                data = {
                    'message': 'hello'
                }
                ws.send(json.dumps(data))
                time.sleep(1)
            except Exception as e:
                print(e)
                break
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


def start():
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://127.0.0.1:8000/ws/chat/user/123",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()


def test():
    import requests
    url = 'http://47.97.94.0:12082/task.do?msg_type=901'
    data = {
        "step": 4,
        "client_type": 1,
        "uuid": "2000f74f-8a6e-11e8-80e8-3497f69bec3c"
    }
    while True:
        try:
            r = requests.post(url, json=data)
            time.sleep(1)
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    start()
    # test()
