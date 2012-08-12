#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks for plaintext of MD5 hash using online service
"""
import urllib2
from connect import conn
import sys

def crack(hashm):
    """Connect and check hash"""
    try:
        data = conn('http://md5.hashcracking.com/search.php?md5=%s' % (hashm))
    except urllib2.URLError:
        print '\nError connecting'
        sys.exit(1)
    else:
        if data == 'No results returned.':
            return False
        else:
            return data