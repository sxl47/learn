#!/usr/bin/env python
# encoding: utf-8

"""
@version: 1.0
@author: sxl
@file: test_gzip.py
@time: 2018/3/30 10:57
@desc:

"""

import gzip
import binascii
from StringIO import StringIO


def gzip_compress(raw_data):
    buf = StringIO()
    f = gzip.GzipFile(mode='wb', fileobj=buf)
    try:
        f.write(raw_data)
    finally:
        f.close()
    return buf.getvalue()


def gzip_uncompress(c_data):
    buf = StringIO(c_data)
    f = gzip.GzipFile(mode='rb', fileobj=buf)
    try:
        r_data = f.read()
    finally:
        f.close()
    return r_data


def start():
    in_data = 'hello, world!'
    print(in_data)
    out_data = gzip_compress(in_data)
    with open('1.zip', 'wb') as f:
        f.write(out_data)

    r_data = gzip_uncompress(out_data)
    print(r_data)


if __name__ == '__main__':
    start()
