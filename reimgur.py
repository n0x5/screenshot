#!/usr/bin/env python

# Download all images on a subreddit from imgur.com
#
# Now supports imgur albums and i.redd.it hosted images
# 
# reimgur.py 'subreddit' 2015-01-01 2015-01-10 e.g.
# 'reimgur.py pics 2015-01-01 2015-01-10'
#
# can change the &limit=30 part up to 1000 but im not sure thats a good idea -
# might get banned 

import re
import time
import argparse
import calendar
import urllib.request
from urllib.request import FancyURLopener
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

class GrabIt(urllib.request.FancyURLopener):
    def __init__(self):
        self.version = ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                     ' (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36')
        urllib.request.FancyURLopener.__init__(self)
    def download_file(self, url, outpath):
        successful = True
        try:
            urlretrieve = GrabIt().retrieve
            urlretrieve(url, outpath)
            return successful
        except Exception:
            successful = False
            return successful


response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
grab1 = GrabIt()

print("searching", url)

def get_single(soup, grab1):
    for link in soup.findAll(string=re.compile("i.imgur.com")):
        link2 = re.sub(r"[?]\d", "", link)
        if os.path.isfile(link2[-11:]):
            print('file exists - skipping')
        else:
            try:
                grab1.download_file(link2, link2[-11:])
                print(link)
            except:
                continue

def get_album(soup, headers, grab1):
    for link in soup.findAll(string=re.compile("imgur.com/a/")):
        print(link)
        response2 = requests.get(link, headers=headers)
        soup2 = BeautifulSoup(response2.text, "html.parser")
        for link2 in soup2.findAll('img', src=re.compile('\/\/i.imgur.com\/\w\w\w\w\w\w\w(.jpg)')):
            link3 = link2['src']
            if os.path.isfile(link3[-11:]):
                print('file exists - skipping')
            else:
                try:
                    grab1.download_file(link3, link3[-11:])
                    print(link3)
                except:
                    continue

def get_reddit_img(soup, grab1):
    for link3 in soup.findAll(string=re.compile("i.redd.it")):
        if os.path.isfile(link3[-16:]):
            print('file exists - skipping')
        else:
            try:
                grab1.download_file(link3, link3[-16:])
                print(link3)
            except:
                continue

get_single(soup, grab1)
get_album(soup, headers, grab1)
get_reddit_img(soup, grab1)
