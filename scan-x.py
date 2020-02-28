#!/usr/bin/env python3
# quick port checker

import ipaddress
import os
import socket
import subprocess
import sys

'''port range set'''
port = str(sys.argv[1])
if port.find(',') != -1:
    portList = list(port.split(',')[0:])
elif port.find('-') != -1:
    portRange = list(port.split('-')[0:])
    portList = []
    for _ in range(int(portRange[0]),int(portRange[1])+1):
        portList.append(str(_))
else:
    portList = [port]

'''ip range set'''
ipSwitch = sys.argv[2]
if ipSwitch == '-c':
    '''ip cidr range ex. 192.168.0.0/28'''
    ipList = list(ipaddress.ip_network(sys.argv[3]))
elif ipSwitch == '-l':
    '''ip list separated by spaces ex. 192.168.2.1 192.168.2.2 192.168.2.3 192.168.2.4 192.168.2.5 192.168.2.6'''
    ipList = list(sys.argv[3:])
elif ipSwitch == '-r':
    '''ip range ex. 192.168.0.2-192.168.1.3'''
    ipRange = sys.argv[3]
    ipRangeStart = ipaddress.ip_address(ipRange.split('-')[0])
    ipRangeEnd = ipaddress.ip_address(ipRange.split('-')[1])
    ipList = []
    while ipRangeStart <= ipRangeEnd:
        ipList.append(str(ipRangeStart))
        ipRangeStart += 1
elif ipSwitch == '-f':
    '''ip addresses listed in a txt file ex. /home/user/scanx.py'''
    ipFile = open(sys.argv[3], 'r')
    ipList = []
    for line in ipFile:
        ipList.append(str(line.strip('\n')))

'''main scanner loop'''
for ipx in ipList:
    with open(os.devnull, 'w') as DEVNULL:
        try:
            subprocess.check_call(['ping', '-c', '1', ipx], stdout=DEVNULL, stderr=DEVNULL)
            is_up = True
        except subprocess.CalledProcessError:
            is_up = False
        if is_up == True:
            try:
                remoteServerIP = socket.gethostbyaddr(ipx)[0]
            except:
                print('Exception ! Host {} does not have a dns entry.'.format(ipx))
                remoteServerIP = 'unknown'
            for portx in portList:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(.25)
                result = sock.connect_ex((ipx, int(portx)))
                if result == 0:
                    print('Host {} ({}) is up and listening on port {} !'.format(ipx, remoteServerIP, portx))
                sock.shutdown(socket.SHUT_RDWR)
                sock.close()
        elif is_up == False:
            print('Exception ! Host {} is not responding to ping. Continuing to the next IP.'.format(ipx))
            continue
sys.exit(0)
