#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks for XSS vulnerabilities on sites returned from crawler
"""
import urllib2
import threading
import Queue
import re
from connect import conn

class Xtest(threading.Thread):
    """Scan for Xss errors and outputs to file"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.xchar = """"><script>alert('xss')</script>"""
        self.file = 'Xss.txt'
 
    def run(self):
        """Checks Url for possible Xss"""
        while True:
            try:
                site = self.queue.get(False)
            except Queue.Empty:
                break
            if '=' in site:
                xsite = site.rsplit('=', 1)[0]
                if xsite[-1] != "=":
                    xsite = xsite + "="
                test = xsite + self.xchar
                try:
                    data = conn(test)
                except urllib2.URLError:
                    self.queue.task_done()
                else:
                    if (re.findall("<script>alert('xss')</script>", data, re.I)):
                        self.xss(test)
                    else:
                        print test + ' <-- Not Vuln'
            else:
                print site + ' <-- No Parameters'
            self.queue.task_done()
 
    def xss(self, url):
        """Proccesses vuln sites into text file and outputs to screen"""
        read = open(self.file, "a+").read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "Xss: " + url
            write = open(self.file, "a+")
            write.write('[XSS]: ' + url + "\n")
            write.close()   