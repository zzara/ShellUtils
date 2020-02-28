#!/usr/bin/env python3
# percent encoder/decoder
# use double quotes or single quotes to wrap your strings
# usage: python3 percent.py encode "alert('not an exploit');"
#        python3 percent.py decode "alert%28%27not%20an%20exploit%27%29%3B"

import sys
from urllib.parse import quote, unquote

p_string = str(sys.argv[2])

if sys.argv[1] == 'encode':
    print(quote(p_string))
elif sys.argv[1] == 'decode':
    print(unquote(p_string))
else:
    print('Expected different args than the ones passed. Please check your commands and try again.')
