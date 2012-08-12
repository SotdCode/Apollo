#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Connect to site and return source
"""
import urllib2
from ua import user_agent

def conn(site):
    """Handle the connection and return source"""
    connection = urllib2.Request(site)
    connection.add_header('User-Agent', user_agent)
    opener = urllib2.build_opener()
    data = opener.open(connection).read() 
    return data