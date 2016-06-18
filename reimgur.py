#!/usr/bin/env python

# Download all images on a subreddit from imgur.com
#
# reimgur.py 'subreddit' 2015-01-01 2015-01-10 e.g.
# 'reimgur.py pics 2015-01-01 2015-01-10'

import re
import time
import argparse
import calendar
import urllib.request
import os
import requests
from bs4 import BeautifulSoup

def crdate(datestr):
    return calendar.timegm(time.strptime(datestr, '%Y-%m-%d'))

parser = argparse.ArgumentParser()
parser.add_argument('subreddit')
parser.add_argument('tstamp1', type=crdate)
parser.add_argument('tstamp2', type=crdate)
args = parser.parse_args()

headers = {
    'User-Agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                   ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
}

url = ('https://www.reddit.com/r/%s/search?q=timestamp%%3A%s..%s&restrict_sr=on&sort=new&t=all&limit=30&syntax=cloudsearch'
       % (args.subreddit, args.tstamp1, args.tstamp2))

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

print("searching", url)
for link in soup.findAll(string=re.compile("i.imgur.com")):
    link2 = re.sub(r"[?]\d", "", link)
    if os.path.isfile(link2[-11:]):
        print('file exists - skipping')
    else:
        try:
            urllib.request.urlretrieve(link2, link2[-11:])
            print(link)
        except:
            continue
