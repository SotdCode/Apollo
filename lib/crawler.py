#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Crawls Ask.com for sites using given dork
"""

import urllib2
import Queue
from connect import conn

def crawl():
    """Crawls Ask.com for sites and sends them to appropriate scan"""
    dork = raw_input('Enter your dork: ')
    queue = Queue.Queue()
    pages = raw_input('How many pages(Max 20): ')
    qdork = urllib2.quote(dork)
    page = 1
    print '\nScanning Ask...'
    for i in range(int(pages)):
        host = "http://uk.ask.com/web?q=%s&page=%s" % (str(qdork), page)
        source = conn(host)
        start = 0
        count = 1
        end = len(source)
        numlinks = source.count('_t" href', start, end)

        while count < numlinks:
            start = source.find('_t" href', start, end)
            end = source.find(' onmousedown="return pk', start,  end)
            link = source[start+10:end-1].replace("amp;","")
            queue.put(link)
            start = end
            end = len(source)
            count = count + 1 
        page += 1
    return queue