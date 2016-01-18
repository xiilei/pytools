#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A hackable http proxy
"""
import logging

from gevent.pywsgi import WSGIServer,WSGIHandler


def application(environ,start_response):
    start_response("200 OK",[("Content-Type", "text/plain; charset=utf-8")])
    return b'hello,world'

if __name__ == '__main__':
    WSGIServer(':8080', application).serve_forever()
