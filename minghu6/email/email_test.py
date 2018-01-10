# -*- coding:utf-8 -*-

import os
import re
import logging
import logging.handlers
import smtplib
import email
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication


class EmailSender:
    class SomeAddrsFailed(Exception):
        pass

    def __init__(self, email_addr, auth_pwd, smtp_addr=None, username=None, logger=None):
        self.email_addr = email_addr
        self.auth_pwd = auth_pwd

        if smtp_addr is None:
            self.smtp_server = EmailSender.guess_smtp_server(self.email_addr)
        else:
            self.smtp_server = smtp_addr

        if username is None:
            self.username = EmailSender.guess_username(self.email_addr)
        else:
            self.username = username

        if logger is None:
            self.logger = EmailSender._init_default_logger('email-sender.log')
        else:
            self.logger = logger

    @staticmethod
    def guess_smtp_server(email_addr):
        return re.sub('(?:.*)@(\w+)(?:\.)(\w+)', r'smtp.\1.\2', email_addr)

    @staticmethod
    def guess_username(email_addr):
        group = re.search('\w+(?=@)', email_addr)

        if group is not None:
            return group.group(0)
        else:
            raise Exception('Can\'t guess email username')

    @staticmethod
    def _init_default_logger(logpath, debug=False):

        default_logger = logging.getLogger('default_logger')

        if debug:
            default_logger.setLevel(logging.DEBUG)
        else:
            default_logger.setLevel(logging.INFO)

        default_formatter = logging.Formatter('%(asctime)-15s [%(levelname)s] %(message)s')

        trh = logging.handlers.TimedRotatingFileHandler(logpath, when='D', interval=1)
        trh.setFormatter(default_formatter)

        sh = logging.StreamHandler()
        sh.setFormatter(default_formatter)

        default_logger.addHandler(trh)
        default_logger.addHandler(sh)

        return default_logger

    # def attach_files(self, file_paths):
    #     for file_path in file_paths:
    #         att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
    #         att["Content-Type"] = 'application/octet-stream'
    #         # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    #         fn = os.path.basename(file_path)
    #         att["Content-Disposition"] = 'attachment; filename="%s"'%fn
    #         self.message.attach(att)

    # def send(self, receipe, subject, text):
    #     # Create an instance with attachment
    #     self.message = MIMEMultipart()
    #     self.subject = subject
    #     self.message['Subject'] = Header(subject, 'utf-8')
    #     # email plain text
    #     self.message.attach(MIMEText(text, 'plain', 'utf-8'))
    #
    #     try:
    #         smtp_obj = smtplib.SMTP()
    #         smtp_obj.connect(self.smtp_server)
    #         smtp_obj.login(self.username, self.auth_pwd)
    #         smtp_obj.sendmail(self.email_addr, receipe, self.message.as_string())
    #         print("邮件发送成功")
    #     except smtplib.SMTPException as ex:
    #         print(ex)
    #         print("Error: 无法发送邮件")

    def send(self, receiver, extrahdrs, subj, bodytext, attaches=(),
                    bodytextEncoding='utf8',
                    attachesEncodings=None,
                    tracesize=256):

        # if not isinstance(bodytext, str):
        #     bodytext = bodytext.decode(bodytextEncoding)
        # elif not isinstance(bodytext, bytes):
        #     bodytext = bodytext.encode(bodytextEncoding)

        if not attaches:
            msg = Message()
            msg.set_payload(bodytext, charset=bodytextEncoding)
        else:
            msg = MIMEMultipart()
            self._add_attachments(msg, bodytext, attaches,
                                  bodytextEncoding, attachesEncodings)

        hdrenc = 'utf-8'  # default=utf8
        Subj = self._encode_header(subj, hdrenc)  # full header
        From = self._encode_addrheader(self.email_addr, hdrenc)  # email names
        To = [self._encode_addrheader(T, hdrenc) for T in receiver]  # each recip
        Tos = ', '.join(To)  # hdr+envelope

        # add headers to root
        msg['From'] = From
        msg['To'] = Tos  # poss many: addr list
        msg['Subject'] = Subj  # servers reject ';' sept
        msg['Date'] = email.utils.formatdate()  # curr datetime, rfc2822 utc
        recip = To
        for name, value in extrahdrs:  # Cc, Bcc, X-Mailer, etc.
            if value:
                if name.lower() not in ['cc', 'bcc']:
                    value = self._encode_header(value, hdrenc)
                    msg[name] = value
                else:
                    value = [self._encode_addrheader(V, hdrenc) for V in value]
                    recip += value  # some servers reject ['']
                    if name.lower() != 'bcc':  # 4E: bcc gets mail, no hdr
                        msg[name] = ', '.join(value)  # add commas between cc

        recip = list(set(recip))  # 4E: remove duplicates
        fullText = msg.as_string()  # generate formatted msg

        self.logger.info('Sending to...' + str(recip))
        self.logger.info(fullText[:tracesize])

        server = smtplib.SMTP(self.smtp_server)  # this may fail too
        server.connect(self.smtp_server)
        server.login(self.username, self.auth_pwd)
        try:
            failed = server.sendmail(From, recip, fullText)  # except or dict
        except:
            server.close()                                   # 4E: quit may hang!
            raise                                            # reraise except
        else:
            server.quit()

        if failed:
            err_msg = 'Failed addrs:%s\n' % failed
            self.logger.error(err_msg)
            raise EmailSender.SomeAddrsFailed(err_msg)

        self.logger.info('Send exit.')

    def _encode_header(self, headertext, unicodeencoding='utf-8'):
        try:
            headertext.encode('ascii')
        except:
            try:
                hdrobj = email.header.make_header([(headertext, unicodeencoding)])
                headertext = hdrobj.encode()
            except:
                pass         # auto splits into multiple cont lines if needed
        return headertext    # smtplib may fail if it won't encode to ascii

    def _encode_addrheader(self, headertext, unicodeencoding='utf-8'):
        try:
            pairs = email.utils.getaddresses([headertext])   # split addrs + parts
            encoded = []
            for name, addr in pairs:
                try:
                    name.encode('ascii')         # use as is if okay as ascii
                except UnicodeError:             # else try to encode name part
                    try:
                        uni  = name.encode(unicodeencoding)
                        hdr  = email.header.make_header([(uni, unicodeencoding)])
                        name = hdr.encode()
                    except:
                        name = None              # drop name, use address part only
                joined = email.utils.formataddr((name, addr))  # quote name if need
                encoded.append(joined)

            fullhdr = ', '.join(encoded)
            if len(fullhdr) > 72 or '\n' in fullhdr:      # not one short line?
                fullhdr = ',\n '.join(encoded)            # try multiple lines
            return fullhdr
        except:
            return self._encode_header(headertext)

    def _add_attachments(self, mainmsg, bodytext, attaches,
                         bodytextEncoding, attachesEncodings):
        """
        format a multipart message with attachments;
        use Unicode encodings for text parts if passed;
        """
        # add main text/plain part
        msg = MIMEText(bodytext, _charset=bodytextEncoding)
        mainmsg.attach(msg)

        # add attachment parts
        encodings = attachesEncodings or (['utf-8'] * len(attaches))
        for (filename, fileencode) in zip(attaches, encodings):
            # filename may be absolute or relative
            if not os.path.isfile(filename):  # skip dirs, etc.
                continue

            # guess content type from file extension, ignore encoding
            contype, encoding = mimetypes.guess_type(filename)
            if contype is None or encoding is not None:  # no guess, compressed?
                contype = 'application/octet-stream'  # use generic default
            self.logger.debug('Adding ' + contype)

            # build sub-Message of appropriate kind
            maintype, subtype = contype.split('/', 1)
            if maintype == 'text':  # 4E: text needs encoding
                if fileencode:  # requires str or bytes
                    data = open(filename, 'r', encoding=fileencode)
                else:
                    data = open(filename, 'rb')
                msg = MIMEText(data.read(), _subtype=subtype, _charset=fileencode)
                data.close()

            elif maintype == 'image':
                data = open(filename, 'rb')  # 4E: use fix for binaries
                msg = MIMEImage(
                    data.read(), _subtype=subtype)
                data.close()

            elif maintype == 'audio':
                data = open(filename, 'rb')
                msg = MIMEAudio(
                    data.read(), _subtype=subtype)
                data.close()

            elif maintype == 'application':  # new  in 4E
                data = open(filename, 'rb')
                msg = MIMEApplication(
                    data.read(), _subtype=subtype)
                data.close()

            else:
                data = open(filename, 'rb')  # application/* could
                msg = MIMEBase(maintype, subtype)  # use this code too
                msg.set_payload(data.read())
                data.close()  # make generic type
            # email.encoders.encode_base64(msg)        # encode using base64
            self.logger.debug('add attachment %s'%filename)

            # set filename (ascii or utf8/mime encoded) and attach to container
            basename = self._encode_header(os.path.basename(filename))
            msg.add_header('Content-Disposition',
                           'attachment', filename=basename)
            mainmsg.attach(msg)

        # text outside mime structure, seen by non-MIME mail readers
        mainmsg.preamble = 'A multi-part MIME format message.\n'
        mainmsg.epilogue = ''  # make sure message ends with a newline


if __name__ == '__main__':
    pass
