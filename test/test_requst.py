#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_requst.py
@time: 2018/12/7 16:21:45
@desc:

"""
import requests


def start():
    headers = {
        "User-Agent": "Baiduspider",
        # "User-Agent": "24HTTrack21421",
    }
    r = requests.get('http://122.114.126.123/', headers=headers)
    print(r.text)


if __name__ == '__main__':
    start()
