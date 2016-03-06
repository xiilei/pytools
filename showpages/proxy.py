#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
A hackable http proxy
"""
from gevent import monkey; monkey.patch_all()
from six.moves.urllib.parse import urlparse
from gevent.pywsgi import WSGIServer,WSGIHandler
from requests import request

from webdriver import browser

def get_dist(environ):
    if environ.get('wsgi.url_scheme') == 'https':
        return False,'',None,None
    host = environ.get('HTTP_HOST', '')
    scriptname = environ.get('SCRIPT_NAME', '')
    pathinfo = environ.get('PATH_INFO', '')
    if pathinfo.startswith("http://"):
        url = pathinfo
    elif host:
        url = 'http://%s%s%s' % (host,scriptname,pathinfo)
    else:
        url = 'http://%s' % pathinfo
    if environ.get('QUERY_STRING', ''):
        url += '?' + environ['QUERY_STRING']
    return environ['REQUEST_METHOD'],url

def get_body(environ):
    return environ['wsgi.input'].read().strip()

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

def get_request(environ):
    method,url = get_dist(environ)
    if not method:
        return None
    req = {'method':method,'url':url,'body':None,'headers':get_headers(environ)}
    if method == 'GET':
        req['body'] = get_body(environ)
    return req

def is_visible_request(req,res):
    '''
    return http request is visible by bowser
    '''
    if req['method'] != 'GET':
        return False
    if req['headers'].get('X-Requested-With') is 'XMLHttpRequest':
        return False
    content_type = res.headers.get('Content-Type','')
    if not content_type.startswith('text/html'):
        return False
    doctype = res.text.lstrip()[0:9]
    if doctype.upper() != u'<!DOCTYPE':
        return False
    return True

def show_page(req,res):
    if is_visible_request(req,res):
        browser.get(req['url'])
    pass

def application(environ,start_response):
    req = get_request(environ)
    if not req:
        start_response('502 Bad Gateway', [('Content-Type', 'text/html')])
    elif req['method'] == 'CONNECT':
        start_response('502 Bad Gateway', [('Content-Type', 'text/html')])
    else:
        try:
            res = request(
                req['method'],
                req['url'],
                headers=req['headers'],
                data=req['body'],
                allow_redirects=False)
            start_response("%d %s" % (res.status_code,res.reason),start_headers(res.headers))
            show_page(req,res)
            return res.content
        except:
            start_response('502 Bad Gateway', [('Content-Type', 'text/html')])

if __name__ == '__main__':
    WSGIServer(':8080', application=application).serve_forever()
