#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks current Ip address using cmyip.com
"""

import urllib2
from connect import conn

def check():
    """Connect to site and grab Ip address"""
    try:
         data = conn('http://cmyip.com/')
    except urllib2.URLError:
        print 'Error connecting'
        return None
    else:
        start = 0
        end = len(data)     
        start = data.find('<title>', start, end)
        end = data.find('-', start, end)   
        ip_add = data[start+25:end-2].strip()
        return ip_add