#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks for common sub domains on a given domain
"""

import urllib2
import threading
import Queue
import socket
from connect import conn

class SDtest(threading.Thread):
    """Checks given Domain for Sub Domains"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
 
    def run(self):
        """Checks if Sub Domain responds"""
        socket.setdefaulttimeout(3)
        while True:
            try:
                domain = self.queue.get(False)
            except Queue.Empty:
                break
            try:
                test = 'http://' + domain
                conn(test)
            except urllib2.URLError:
                pass
            else:
                target = socket.gethostbyname(domain)  
                print 'Found: ' + test + ' - ' + target
            finally:
                self.queue.task_done()        
 

def subd(site):
    """Create queue and threads for sub domain scans"""
    queue = Queue.Queue()
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
    return queue