# -*- coding: utf-8 -*-

import os, sys, json, re, argparse, urllib2, html5lib
from bs4 import BeautifulSoup, Tag, UnicodeDammit
import pandas as pd
from pandas.io.json import json_normalize
import time

import re
import operator
import math


def get_script(url):
    #load script
    script_url = url
    is_webpage_fetched = False
    request_headers = {
    "Accept-Language": "en-US,en;q=0.5",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    #"Connection": "keep-alive" 
    }


    while not is_webpage_fetched:
        # get the script's URL from the parameters if it was passed
        try:
            request = urllib2.Request(script_url, headers=request_headers)
            contents = urllib2.urlopen(request)#.read()
            soup = BeautifulSoup(contents, 'lxml')
            print('Detected encoding is ', soup.original_encoding)
            is_webpage_fetched = True
        except urllib2.URLError as err:
            print('Catched an URLError while fetching the URL:', err)
            pass
        except ValueError as err:
            print('Catched a ValueError while fetching the URL:', err)
            pass
        except:
            print('Catched an unrecognized error')
            raise
        else:
            #script_text = soup.find("td", class_="scrtext").find("pre")
            script_text = soup.find("pre")

            if( script_text.find("pre") ):
                print('Found a <pre> inside the <pre>')
                script_text = script_text.find("pre")
            is_webpage_fetched = True
    print('Getting script @ %s.' %(url))
    return script_text


