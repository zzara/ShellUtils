#!/bin/env python3
# scrape contents of tags from a single web page to a txt file

import sys
import bs4
import urllib.request

def request_maker(url,file):
    swarmUrl = str(url)
    swarmHeaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    swarmReq = urllib.request.Request(swarmUrl, data=None, headers=swarmHeaders)
    swarmResp = urllib.request.urlopen(swarmReq)
    swarmContent = swarmResp.read()
    tags = ['h1','h2','h3','h4','h5','h6','h7','p','li']
    soup = bs4.BeautifulSoup(swarmContent,'lxml')
    for element in soup.find_all(tags):
        file_out = open('output_html.txt', 'a')
        file_out.write(str(element.text))
        file_out.close()
    soup.decompose()

request_maker('https://docs.python.org/3/library/urllib.request.html#urllib.request.Request.add_header','output.txt')
