#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#only supported in linux


__author__ = 'xilei'

from struct import pack, unpack, calcsize


def arppacket():
    """
    先简单加个实例
    """
    bcast_mac = pack('!6B', *(0xFF,)*6)
    sender_mac = pack('!6B', *(0xC0, 0xD9, 0x62, 0x1F, 0x2F, 0x9C))
    target_mac = pack('!6B', *(0xC0, 0xD9, 0x62, 0x1F, 0x2F, 0x9C))
    #pack('!H', 0x0001)
    arpop = pack('!H', 0x0001)

    ip = '192.168.1.1'
    target_ip = '192.168.1.255'
    sender_ip = pack('!4B', *[int(x) for x in ip.split('.')])
    target_ip = pack('!4B', *[int(x) for x in target_ip.split('.')])

    socket_mac = sender_mac
    arpframe = [
        ### ETHERNET
        # destination MAC addr
        bcast_mac,
        # source MAC addr
        socket_mac,
        # protocol type (=ARP)
        pack('!H', 0x0806),

        ### ARP
        # logical protocol type (Ethernet/IP)
        pack('!HHBB', 0x0001, 0x0800, 0x0006, 0x0004),
        # operation type
        arpop,
        # sender MAC addr
        sender_mac,
        # sender IP addr
        sender_ip,
        # target hardware addr
        target_mac,
        # target IP addr
        target_ip
    ]
    return b''.join(arpframe)


def sender():
    pass


if __name__ == "__main__":
    pass


