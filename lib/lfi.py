#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks for LFI vulnerabilities on sites returned from crawler
"""

import threading
import Queue
import urllib2
from connect import conn
import re


class Ltest(threading.Thread):
    """Scans for Lfi errors and outputs to file"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.file = 'Lfi.txt'
        self.queue = queue
        self.lchar = '../' 
       
    def run(self):
        """Checks Url for File Inclusion errors"""
        while True:
            try:
                site = self.queue.get(False)
            except Queue.Empty:
                break
            if '=' in site:
                lsite = site.rsplit('=', 1)[0]
                if lsite[-1] != "=":
                    lsite = lsite + "="
                test = lsite + self.lchar
                try:
                    data = conn(test)
                except urllib2.URLError:
                    self.queue.task_done()
                else:
                    if (re.findall("failed to open stream: No such file or directory", data, re.I)):
                        self.lfi(test)
                    else:
                        print test + ' <-- Not Vuln'
            else:
                print site + ' <-- No Parameters' 
            self.queue.task_done()

    def lfi(self, url):
        """Adds vulns to file and prints to screen"""
        read = open(self.file, "a+").read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "Lfi: " + url
            write = open(self.file, "a+")
            write.write('[LFI]: ' + url + "\n")
            write.close()   