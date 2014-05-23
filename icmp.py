#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'xilei'

import os
import sys
import time
import array
import socket

import getopt
from threading import Thread
from struct import pack, unpack, calcsize


class SenderThread(Thread):

    def __init__(self, sock, cid, ip, total=4):
        Thread.__init__(self)
        self._sock = sock
        self._total = total
        self._cid = cid
        self._ip = ip

    def run(self):
        for i in range(self._total):
            try:
                self._sock.sendto(icmppacket((i+1), self._cid), (self._ip, 0))
            except socket.error as se:
                print(se)
                break
            finally:
                time.sleep(1)


def ping(ip, total=4, ipv6=False):
    """
    simple ping
    """
    ipv6 = ipv6 and socket.has_ipv6 or False
    #sock.bind(('wlan0', socket.SOCK_RAW))
    family = ipv6 and socket.AF_INET6 or socket.AF_INET
    try:
        sock = socket.socket(family, socket.SOCK_RAW, socket.getprotobyname('icmp'))
        sock.settimeout(6)
    except socket.error as ie:
        print(ie)
        return

    cid = os.getpid() & 0xffffff

    sender = SenderThread(sock, cid, ip, total)
    sender.start()

    rc = 0
    while rc < total:
        try:
            recv_packet, addr = sock.recvfrom(1024)
            recv_time = time.time()
            head = recv_packet[20:28]
            # I think so ...
            ttl, = unpack('B', recv_packet[8:9])
            type1, code, checksum1, packet_id, sequence = unpack("BBHHh", head)
            if packet_id == cid:
                send_time = unpack("d", recv_packet[28:28 + calcsize('d')])[0]
                print("reply:%s seq=%s ttl=%s time:%.2fms" % (addr[0], sequence/256, ttl, (recv_time-send_time)*1000))
        except socket.error as _re:
            print(_re)
            break
        finally:
            rc += 1
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


#todo padding
def icmppacket(sequence=1, cid=98, ipv6=False, psize=64):
    #type,code,Checksum,ID,Sequence
    sequence *= 256
    psize -= 8
    head = pack('BBHHh', 8, 0, 0, cid, sequence)
    data = pack('d', time.time())+pack('Q', psize-calcsize("d"))
    csum = checksum(head+data)
    return pack('BBHHh', ipv6 and 128 or 8, 0, csum, cid, sequence)+data

#todo KeyboardInterrupt
if __name__ == "__main__":
    _ip = ''
    _total = 4
    _ipv6 = False
    opts = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:t:i6", ["ip=", "total=", "ipv6"])
    except getopt.GetoptError as e:
        print(e)
        sys.exit(0)
    for opt, arg in opts:
        if opt in ("-i", "--ip"):
            _ip = arg.strip()
        if opt in ("-t", "--total"):
            _total = int(arg)
        if opt in ("-i6", "--ipv6"):
            _ipv6 = True

    if len(_ip) >= 8:
        ping(_ip, _total)
    else:
        print("invalid params,use like -i 192.168.1.1")
