#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks for RFI vulnerabilities on sites returned from crawler
"""

import urllib2
import Queue
import threading
import re
from connect import conn

class Rtest(threading.Thread):
    """Scans for Rfi vulns and outputs to file"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.file = 'Rfi.txt'
 
    def run(self):
        """Checks Url for Remote File Inclusion vulnerability"""
        while True:
            try:
                site = self.queue.get(False)
            except Queue.Empty:
                break
            if '=' in site:
                rsite = site.rsplit('=', 1)[0]
                if rsite[-1] != "=":
                    rsite = rsite + "="
                link = rsite + 'http://google.com' + '?'
                try:
                    data = conn(link)
                except urllib2.URLError:
                    self.queue.task_done()
                else:
                    if (re.findall("""<meta content="Search the world's information, including webpages, images, videos and more.""", data, re.I)): 
                        self.rfi(link)
                    else:
                        print link  + ' <-- Not Vuln'
            else:
                print site + ' <-- No Parameters'   
            self.queue.task_done()
            
    def rfi(self, url):
        """Proccesses vuln sites into text file and outputs to screen"""
        read = open(self.file, "a+").read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "Rfi: " + url
            write = open(self.file, "a+")
            write.write('[Rfi]: ' + url + "\n")
            write.close() 