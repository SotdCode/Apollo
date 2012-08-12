#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Checks for admin login pages on target site
"""

from connect import conn
import urllib2
import threading
import Queue

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
                conn(site)
            except urllib2.URLError:
                pass
            else:
                print 'Found: %s' % (site)
            finally:
                self.queue.task_done()


def acheck(site):
    """Create queue and threads for admin page scans"""
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
    return queue
        