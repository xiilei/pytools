#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A hackable http proxy
"""
import logging

from six.moves.urllib.parse import urlparse
from gevent.pywsgi import WSGIServer,WSGIHandler

def get_dist(environ):
    keys = ('PATH_INFO','HTTP_HOST')
    host = ''
    port = 80
    if environ.get('wsgi.url_scheme') == 'https':
        return False,443
    for k in keys:
        host = environ.get(k,'')
        if not host:
            continue
        if host.startswith('http'):
            host = host[7:].lstrip('/')
        host_partail = host.split(':')
        if len(host_partail)==2:
            return host_partail[0],int(host_partail[1])
        return host,port

def get_url(environ):
    pass

def is_visible_request():
    '''
    return http request is visible by user's bowser
    '''
    return False

def proxy_request():
    pass

def application(environ,start_response):
    host,port = get_dist(environ)
    if not host:
        start_response('501 Not Implemented', [])
    else:
        start_response("200 OK",[("Content-Type", "text/plain; charset=utf-8")])
        return b'request to %s:%d' % (host,port)

if __name__ == '__main__':
    WSGIServer(':8080', application).serve_forever()
