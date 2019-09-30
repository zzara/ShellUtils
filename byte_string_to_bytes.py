# -*- coding: utf-8 -*-
#/usr/bin/python3.7

"""String representation of bytes back to bytes"""

def byte_string_to_bytes(string):
    bytez = b''
    for i in string:
        try:
            bytez += struct.pack("B", ord(i))
        except: pass
    return bytez

# then decode as utf, unicode, etc
# print(count_string_to_bytes('something').decode('unicode-escape'))
