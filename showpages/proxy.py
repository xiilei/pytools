#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A hackable http proxy
"""
import logging

import requests
from six.moves.urllib.parse import urlparse
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer,WSGIHandler

def get_dist(environ):
    if environ.get('wsgi.url_scheme') == 'https':
        return False,'',None,None
    url = environ['PATH_INFO']
    if environ['QUERY_STRING']:
        url += '?'+environ['QUERY_STRING']
    method = environ['REQUEST_METHOD']
    body = None
    headers = {
        'user-agent':environ.get('HTTP_USER_AGENT','Chrome Linux')
    }
    if method != 'GET':
        body = env['wsgi.input'].read().strip()
    return method,url,body,headers

def is_visible_request():
    '''
    return http request is visible by user's bowser
    '''
    return False

def proxy_request():
    pass

def application(environ,start_response):
    method,url,body,headers = get_dist(environ)
    if not method:
        start_response('501 Not Implemented', [])
    else:
        if method == 'GET':
            r = requests.get(url,headers=headers)
            print(r.reason)
            start_response("%d %s" % (r.status_code,r.reason),[("Content-Type", "text/html; charset=utf-8")])
            return r.content
if __name__ == '__main__':
    WSGIServer(':8080', application).serve_forever()
