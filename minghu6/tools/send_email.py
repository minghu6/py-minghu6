# -*- coding:utf-8 -*-

"""SEND_EMAIL

Usage:
  send_email <from> <to> <subj> <body> [--attachments=<attachments>...] [--password=<password>] [--cc=<cc>] [--bcc=<bcc>]

Options:
  <from>  from email address
  <to>    to email address
  <subj>  subject of the email
  <body>  body of the email

  -att --attachment=<attachments>  attach paths
  -p --password=<password>         user password
  -cc --cc=<cc>...                 cc split with ":" or ";" based on OS
  -bcc --bcc=<bcc>...              bcc split with ":" or ";" based on OS

"""

from docopt import docopt
from minghu6.etc.cmd import env_sep
from minghu6.email.email_test import EmailSender


def cli():
    arguments = docopt(__doc__)

    email_sender = EmailSender(arguments['<from>'], arguments['--password'] if arguments['--password'] else None)

    cc = arguments['--cc'].split(env_sep) if arguments['--cc'] else ()
    bcc = arguments['--bcc'].split(env_sep) if arguments['--bcc'] else ()

    print(cc)
    print(bcc)
    email_sender.send([arguments['<to>']],
                      [('cc', cc), ('bcc', bcc)],
                      arguments['<subj>'],
                      arguments['<body>'],
                      arguments['--attachments'])


if __name__ == '__main__':
    cli()
