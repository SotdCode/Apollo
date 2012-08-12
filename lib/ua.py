#!/usr/bin/env python
# -*- coding: UTF-8 -*

"""
Returns a random user user_agent
"""
from random import choice

USER_AGENT = ["Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3",
             "Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.7) Gecko/20100809 Fedora/3.6.7-1.fc14 Firefox/3.6.7",
             "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
             "Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)",
             "YahooSeeker/1.2 (compatible; Mozilla 4.0; MSIE 5.5; yahooseeker at yahoo-inc dot com ; http://help.yahoo.com/help/us/shop/merchant/)",
             "Opera/9.00 (Windows NT 5.1; U; en)",
             "Mozilla/2.0 (compatible; Ask Jeeves)",
             "Mozilla/4.0 (compatible; MSIE 5.0; Windows NT 5.1; .NET CLR 1.1.4322)"
            ]

def user_agent():
    return choice(USER_AGENT)
