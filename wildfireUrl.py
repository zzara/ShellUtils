#!/bin/env python
# extract urls from wildfire reports
import requests
import re

dataParams = {'apikey':'<api_key>', 'hash':'<mal_hash>', 'format':'xml'}
reqPost= requests.post('https://wildfire.paloaltonetworks.com/publicapi/get/report', data=dataParams)
match = re.findall('<url host="(.*?)"', reqPost.text, re.IGNORECASE)
match2 = re.findall('http://(.*?)/', reqPost.text, re.IGNORECASE)
mergedList = list(set(match + match2))
regex = re.compile(r'[0-9]$')
filtered = [i for i in mergedList if not regex.search(i)]
if filtered:
    print(filtered)
