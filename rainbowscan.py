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
parser.add_argument('-i', '--host', action="store")
parser.add_argument('-u', '--udp', action="store_true")
parser.add_argument('-s', '--syn', action="store_true")
parser.add_argument('-t', '--tcp', action="store_true")
parser.add_argument('-i', '--icmp', action="store_true")
parser.add_argument('-r', '--rainbow', action="store_true")

args = parser.parse_args()

print('scanning the crap out of {}...'.format(sys.argv[1]))
for _ in range(1,1000):
    if args.icmp:
        # icmp scan
        network_layer = IP(dst=args.host)
        sr(network_layer/ICMP(), retry=0, timeout=0.001, verbose=False)
        print('syn packet sent to port {}'.format(_))

    if args.syn:
        # synscan
        network_layer = IP(dst=args.host)
        transport_layer = TCP(dport=_, flags="S")
        send(network_layer/transport_layer, verbose=False)
        print('syn packet sent to port {}'.format(_))

    if args.udp:
        # udp scan
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.01)
        result = sock.connect_ex((args.host, _))
        print('connecting to port {}'.format(_))
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()

    if args.tcp:
        # tcp scan
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(.01)
        result = sock.connect_ex((args.host, _))
        print('connecting to port {}'.format(_))
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
