import socket
from struct import pack, unpack, calcsize

ARPOP_REQUEST = pack('!H', 0x0001)
ARPOP_REPLY = pack('!H', 0x0002)
BCAST_MAC =  pack('!6B', *(0xFF,)*6)

def arp_packet(target_ip,target_mac,sender_ip,sender_mac,arp_type=ARPOP_REQUEST):
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

#the raw l2 socket
def create_l2sock(device):
    sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(0x806))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 0)
    sock.bind((device, 0x806))
    return sock