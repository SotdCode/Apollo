#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks for routers running SSH using default user/passw in a given Ip range
"""

import Queue
import threading
import paramiko

class Routers(threading.Thread):
    """Checks for routers running ssh with given User/Pass"""
    def __init__(self, queue, user, passw):
        threading.Thread.__init__(self)     
        self.queue = queue 
        self.user = user
        self.passw = passw
 
    def run(self):
        """Tries to connect to given Ip on port 22"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        while True:
            try:
                ip_add = self.queue.get(False)
            except Queue.Empty:
                break
            try:
                ssh.connect(ip_add, username = self.user, password = self.passw, timeout = 10)
                ssh.close()
            except:
                print 'Not Working: %s:22 - %s:%s\n' % (ip_add, self.user, self.passw)
            else:
                print "Working: %s:22 - %s:%s\n" % (ip_add, self.user, self.passw)
                write = open('Routers.txt', "a+")
                write.write('%s:22 %s:%s\n' % (ip_add, self.user, self.passw))
                write.close()  
            finally:
                self.queue.task_done()

def iprange(start_ip, end_ip):
    """Creates list of Ip's from Start_Ip to End_Ip"""
    queue = Queue.Queue()
    ip_range = []
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    tmp = start
   
    ip_range.append(start_ip)
    while tmp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if tmp[i] == 256:
                tmp[i] = 0
                tmp[i-1] += 1
        ip_range.append(".".join(map(str, tmp)))
   
    for add in ip_range:
        queue.put(add)
    return queue