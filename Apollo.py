#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
      Apollo.py - Python Vulnerability Scanner -
       Written by Sotd - twitter.com/#!/Sotd_
"""            

#For dorks don't include inurl: , Eg: Enter your dork: main.php?id=
try:
    from lib.router import iprange, Routers
    PARAMIKO = True
except ImportError:
    PARAMIKO = False

from lib.crawler import crawl
from lib.sqli import Stest
from lib.ipcheck import check
from lib.cracker import crack
from lib.lfi import Ltest
from lib.xss import Xtest
from lib.rfi import Rtest
from lib.admin import acheck, Atest
from lib.subd import subd, SDtest
from random import choice
import time
import sys

def main():
    """Outputs Menu and gets input. Runs scans"""
    red = "\033[01;31m{0}\033[00m"
    quotes = [
         '\n"Three things cannot be long hidden: the sun, the moon, and the truth."\n', 
         '\n"Nothing holds it together except an idea which is indestructible"\n', 
         '\n"I am not a liberator. Liberators do not exist. The people liberate themselves."\n', 
         '\n"Heresy is just another word for freedom of thought".\n', 
         '\n"The tragedy of modern war is that the young men die fighting each other - instead of their real enemies back home in the capitals"\n', 
         '\n"A man is no less a slave because he is allowed to choose a new master once in a term of years."\n'
        ]
    print red.format('''
            _____       _       _
           /  ___|     | |     | |
           \ `--.  ___ | |_  __| |
            `--. \/ _ \| __|/ _` |
           /\__/ / (_) | |_  (_| |
           \____/ \___/ \__|\__,_|
                     
#################################################
#                                    |          #
#                                  \ _ /        #
#           Welcome to Apollo    -= (_) =-      #                           
#Options:                          /   \        #
#[1] Sqli                            |          #
#[2] Lfi                                        #
#[3] Xss                                        #
#[4] Rfi                                        #
#[5] Routers                                    #
#[6] Admin Page Finder                          #
#[7] Sub Domain Scan                            #
#[8] Online MD5 cracker                         #
#[9] Check IP                                   #
#################################################
''')
    option = raw_input('Enter Option: ')
 
    if option:
        if option == '1':
            sites = crawl()
            for i in range(10):
                thread = Stest(sites)
                thread.setDaemon(True)
                thread.start() 
            sites.join()
            print red.format(choice(quotes))
            
        elif option == '2':
            sites = crawl()
            for i in range(10):
                thread = Ltest(sites)
                thread.setDaemon(True)
                thread.start() 
            sites.join()
            print red.format(choice(quotes))
 
        elif option == '3':
            sites = crawl()
            for i in range(10):
                thread = Xtest(sites)
                thread.setDaemon(True)
                thread.start() 
            sites.join()
            print red.format(choice(quotes))
 
        elif option == '4':
            sites = crawl()
            for i in range(10):
                thread = Rtest(sites)
                thread.setDaemon(True)
                thread.start() 
            sites.join()
            print red.format(choice(quotes))
     
        elif option == '5':
            if not PARAMIKO:
                print 'Paramiko module needed'
                print 'http://www.lag.net/paramiko/'
                sys.exit(1)
            start_ip = raw_input('Start ip: ')
            end_ip = raw_input('End ip: ')
            user = raw_input('User: ')
            passw = raw_input('Password: ')
            targets = iprange(start_ip, end_ip)
            for i in range(10):
                thread = Routers(targets, user, passw)
                thread.setDaemon(True)
                thread.start() 
            targets.join()
            print red.format(choice(quotes))
 
        elif option == '6':
            print 'Need to include http:// and ending /\n'
            site = raw_input('Site: ')
            if 'http://' not in site:
                site = 'http://' + site
            if site[-1] != '/':
                site = site + '/'
            targets = acheck(site)
            for i in range(10):
                thread = Atest(targets)
                thread.setDaemon(True)
                thread.start() 
            targets.join()
            print red.format(choice(quotes))

        elif option == '7':
            site = raw_input('Domain: ')
            targets = subd(site)
            for i in range(10):
                thread = SDtest(targets)
                thread.setDaemon(True)
                thread.start() 
            targets.join()
            print red.format(choice(quotes))

        elif option == '8':
            hashm = raw_input('Enter MD5 Hash: ')
            result = crack(hashm)
            if result:
                print '\n- %s -' % (result)
            else:
                print '\n- Not found or not valid -'
            print red.format(choice(quotes)) 

        elif option == '9':
            current = check()
            if not current:
                sys.exit(1)
            print "Current Ip address is %s" % (current)
            print red.format(choice(quotes))       

        else:
            print '\nInvalid Choice\n'
            time.sleep(0.5)
            main()    
              
    else:
        print '\nYou Must Enter An Option\n'
        time.sleep(0.5)
        main()
if __name__ == '__main__':
    main()