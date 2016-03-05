#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A hackable http proxy
"""
import logging

from gevent import monkey; monkey.patch_all()
from six.moves.urllib.parse import urlparse
from gevent.pywsgi import WSGIServer,WSGIHandler
import requests

def get_dist(environ):
    if environ.get('wsgi.url_scheme') == 'https':
        return False,'',None,None
    url = environ['PATH_INFO']
    if environ['QUERY_STRING']:
        url += '?'+environ['QUERY_STRING']
    method = environ['REQUEST_METHOD']
    body = None
    if method != 'GET':
        body = environ['wsgi.input'].read().strip()
    return method,url,body

def get_headers(environ):
    headers = {}
    for k,v in environ.iteritems():
        if k.startswith('HTTP_') and v is not '':
            headers[k[5:].replace("_", "-").lower()] = v
    return headers

def start_headers(headers):
    enabled = ('Content-Type','Content-Length','Server','Connection')
    new_headers = []
    for k,v in headers.iteritems():
        if k in enabled:
            new_headers.append((k,v))
    return new_headers

def is_visible_request():
    '''
    return http request is visible by user's bowser
    '''
    return False

def proxy_request():
    pass

def application(environ,start_response):
    method,url,body = get_dist(environ)
    if not method:
        start_response('501 Not Implemented', [])
    else:
        if method == 'GET':
            r = requests.get(url,headers=get_headers(environ))
            start_response("%d %s" % (r.status_code,r.reason),start_headers(r.headers))
            return r.content

if __name__ == '__main__':
    WSGIServer(':8080', application=application).serve_forever()
