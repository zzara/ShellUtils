#!/bin/env python3
# bulk base64 decode
# use with files containing large base64 strings
# usage: python3 dig64.py <input_filepath> <output_filepath>

import base64
import re
import sys
import time
timez = str(time.time())
for line in open(sys.argv[1], 'r'):
    base_find = re.findall(r'[A-Za-z0-9+/]{25,}=?=?',line)
    for item in base_find:
        try:
            base_out = str(base64.b64decode(item))
            if int(str(base_out).count('\\x')) > 20:
                continue
            print(base_out)
            base_write = open('{}/dig64_out_{}.txt'.format(sys.argv[2],timez),'a')
            base_write.write(base_out + '\n')
            base_write.close()
        except:
            pass
