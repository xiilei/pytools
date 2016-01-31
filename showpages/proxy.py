#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A hackable http proxy
"""
import logging

from six.moves.urllib.parse import urlparse
from gevent.pywsgi import WSGIServer,WSGIHandler

def get_dist(environ):
    http_host = environ.get('HTTP_HOST', '').lower()
    http_host_partail = http_host.split(':')
    if len(http_host_partail) == 2:
        return http_host_partail[0], int(http_host_partail[1])
    return http_host,80

def is_visible_request():
    '''
    return http request is visible by user's bowser
    '''
    return False

def proxy_request():
    pass

def application(environ,start_response):
    start_response("200 OK",[("Content-Type", "text/plain; charset=utf-8")])
    host,port = get_dist(environ)
    return b'request to %s:%d' % (host,port)

if __name__ == '__main__':
    WSGIServer(':8080', application).serve_forever()
