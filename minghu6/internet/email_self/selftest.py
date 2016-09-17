#! /usr/bin/env python3
# -*- coding:utf-8 -*-

"""
###############################################################################
self-test when this file is run as a program
###############################################################################
"""

#
#mailconfig mormally comes from the client's sourse directory or sys.path;
#for testing ,get it from Email directory one level up
#
import sys
sys.path.append('..')
import mailconfig
print('config:',mailconfig.__file__)

#get these from __init__,Care:email_self is standard library ??
from minghu6.internet.email_self import (MailFetcherConsole,
                                         MailSender, MailSenderAuthConsole,
                                         MailParser)

if not mailconfig.smtpuser:
    sender=MailSender(tracesize=5000)
else:
    sender=MailSenderAuthConsole(tracesize=5000)

sender.sendMessage(From=mailconfig.myaddress,
                   To=[mailconfig.myaddress],
                   Subj='testing mailtools package',
                   extrahdrs=[('X-Mailer','mailtools')],
                   bodytext='Here is my source code\n',
                   bodytextEncoding='utf8',
                   attaches=['selftest.py'],)

fetcher=MailFetcherConsole()

def status(*args):
    print(args)

hdrs,sizes,loadedall=fetcher.downloadAllHeader(status)
for num,hdr, in enumerate(hdrs[:5]):
    print(hdr)
    if input('load maiol?') in ['y','Y']:
        print(fetcher.downloadMessage(num+1).rstrip(), '\n', '-'*70)

last5=len(hdrs)-4
msgs,sizes,loadedall=fetcher.downloadAllMessages(status,loadfrom=last5)
for msg in msgs:
    print(msg[:200],'\n','-'*70)
parser=MailParser()
for i in [0]:
    fulltext=msgs[i]
    message=parser.parseMessage(fulltext)
    ctype,maintext=parser.findMainText(message)
    print('Parsed:',message['Subject'])
    print(maintext)

input('Press Enter to exit')
