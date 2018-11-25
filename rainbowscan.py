#!/bin/env python3
# synscan
# v0.01a

import argparse
import ipaddress
import os
import socket
import sys

from scapy.layers.inet import IP, TCP, ICMP
from scapy.sendrecv import send, sr

parser = argparse.ArgumentParser()
parser.add_argument('-k', '--host', action="store")
parser.add_argument('-l', '--level', action="store")
parser.add_argument('-u', '--udp', action="store_true")
parser.add_argument('-s', '--syn', action="store_true")
parser.add_argument('-t', '--tcp', action="store_true")
parser.add_argument('-i', '--icmp', action="store_true")
args = parser.parse_args()

if args.level == 'low' or args.level is None:
    level = 20

elif args.level == 'med':
    level = 100

elif args.level == 'low':
    level = 500

elif args.level == 'insane':
    level = 1000

print('scanning the crap out of {}...'.format(sys.argv[1]))
for port in range(1,level):
    if args.icmp:
        # icmp scan
        network_layer = IP(dst=args.host)
        sr(network_layer/ICMP(), retry=0, timeout=0.001, verbose=False)
        print('syn packet sent to port {}'.format(port))

    if args.syn:
        # synscan
        network_layer = IP(dst=args.host)
        transport_layer = TCP(dport=port, flags="S")
        send(network_layer/transport_layer, verbose=False)
        print('syn packet sent to port {}'.format(port))

    if args.udp:
        # udp scan
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(.01)
        sock.sendto(bytes('rainbows', "utf-8"), (args.host, port))
        print('sending to port {}'.format(port))

    if args.tcp:
        # tcp scan
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.01)
        result = sock.connect_ex((args.host, port))
        print('connecting to port {}'.format(port))
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
