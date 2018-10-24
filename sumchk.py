
#!/usr/bin/env python3

import hashlib
import sys
import time

def file_as_bytes(file):
    with file:
        return file.read()

sum1 = hashlib.md5(file_as_bytes(open(sys.argv[1], 'rb'))).hexdigest()

while True:
    sum2 = hashlib.md5(file_as_bytes(open(sys.argv[1], 'rb'))).hexdigest()
    if sum1 not in sum2:
        sum1 = sum2
        print(sum1)
    time.sleep(1)
