#!/bin/env python3
# synscan
# v0.01a

import ipaddress
import os
import socket
import sys

from scapy.layers.inet import IP, TCP, ICMP
from scapy.sendrecv import send, sr

print('scanning the crap out of {}...'.format(sys.argv[1]))
for _ in range(1,1000):
    
    # icmp scan
    #network_layer = IP(dst=sys.argv[1])
    #sr(network_layer/ICMP(), retry=0, timeout=0.001, verbose=False)
    #print('syn packet sent to port {}'.format(_))

    # synscan
    network_layer = IP(dst=sys.argv[1])
    transport_layer = TCP(dport=_, flags="S")
    send(network_layer/transport_layer, verbose=False)
    print('syn packet sent to port {}'.format(_))

    # udp scan
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(.01)
    #result = sock.connect_ex((sys.argv[1], _))
    #print('connecting to port {}'.format(_))
    #sock.shutdown(socket.SHUT_RDWR)
    #sock.close()

    # tcp scan
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.settimeout(.01)
    #result = sock.connect_ex((sys.argv[1], _))
    #print('connecting to port {}'.format(_))
    #sock.shutdown(socket.SHUT_RDWR)
    #sock.close()
