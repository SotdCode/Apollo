#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""Checks for SQLI vulnerabilites on sites returned from crawler
"""

import urllib2
import threading
from connect import conn
import Queue
import re

class Stest(threading.Thread):
    """Scans for Sql errors and ouputs to file"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.schar = "'"
        self.file = 'MySql.txt'
 
    def run(self):
        """Scans Url for Sql errors"""
        while True:
            try:
                site = self.queue.get(False)
            except Queue.Empty:
                break
            if '=' in site:
                test = site + self.schar

                try:
                    data = conn(test)
                except urllib2.URLError:
                    self.queue.task_done()
                else:
                    if (re.findall("You have an error in your SQL syntax", data, re.I)):
                        self.mysql(test)
                    elif (re.findall('mysql_fetch', data, re.I)):
                        self.mysql(test)
                    elif (re.findall('JET Database Engine', data, re.I)):
                        self.mssql(test)
                    elif (re.findall('Microsoft OLE DB Provider for', data, re.I)):
                        self.mssql(test)
                    else:
                        print test + ' <-- Not Vuln'
            else:
                print site + ' <-- No Parameters'
            self.queue.task_done()

    def mysql(self, url):
        """Proccesses vuln sites into text file and outputs to screen"""
        read = open(self.file, "a+").read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "MySql: " + url
            write = open(self.file, "a+")
            write.write(url + "\n")
            write.close()

    def mssql(self, url):
        """Proccesses vuln sites into text file and outputs to screen"""
        read = open('MsSql.txt', "a+").read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "MsSql: " + url
            write = open('MsSql.txt', "a+")
            write.write(url + "\n")
            write.close()   