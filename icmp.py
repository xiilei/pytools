#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'xilei'

import socket
from struct import pack
import time
import array
from threading import Thread


class SenderThread(Thread):

    def __init__(self, sock, packet, ip, total=4):
        Thread.__init__(self)
        self._sock = sock
        self._total = total
        self._packet = packet
        self._ip = ip
        self.count = 0

    def run(self):
        for i in range(self._total):
            try:
                self._sock.sendto(self._packet, (self._ip, 0))
            except socket.timeout:
                break
            finally:
                self.count += 1
            time.sleep(1)


def ping(ip, total=4, ipv6=False):
    ipv6 = ipv6 and socket.has_ipv6 or False
    #sock.bind(('wlan0', socket.SOCK_RAW))
    family = ipv6 and socket.AF_INET6 or socket.AF_INET
    sock = socket.socket(family, socket.SOCK_RAW, socket.getprotobyname('icmp'))
    sock.settimeout(6)
    sender = SenderThread(sock, icmppacket(), ip, total)
    sender.start()
    while True:
        try:
            if sender.count > total-1:
                break
            print(sock.recvfrom(1024))
        except socket.error as e:
            print(e)
            break
        finally:
            if not sender.is_alive():
                break
    sock.close()


def checksum(packet):
    if len(packet) & 1:
        packet = packet + '\0'
    words = array.array('h', packet)
    sum = 0
    for word in words:
        sum += (word & 0xffff)
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    return (~sum) & 0xffff


def icmppacket(ipv6=False):
    #type,code,Checksum,ID,Sequence
    cid = 98
    sequence = 2
    head = pack('BBHHH', 8, 0, 0, cid, sequence)
    data = pack('d', time.time())
    csum = checksum(head+data)
    return pack('BBHHh', ipv6 and 128 or 8, 0, csum, cid, sequence)+data



if __name__ == "__main__":
        ping('192.168.1.1', 4)