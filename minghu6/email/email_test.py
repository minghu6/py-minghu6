# -*- coding:utf-8 -*-

import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

receivers = ['zhaonuge@163.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱


class EmailSender:
    def __init__(self, email_addr, auth_pwd, smtp_addr=None, username=None):
        self.email_addr = email_addr
        self.auth_pwd = auth_pwd

        if smtp_addr is None:
            self.smtp_addr = EmailSender.guess_smtp_addr(self.email_addr)
        else:
            self.smtp_addr = smtp_addr

        if username is None:
            self.username = EmailSender.guess_username(self.email_addr)
        else:
            self.username = username

    @staticmethod
    def guess_smtp_addr(email_addr):
        return re.sub('(?:.*)@(\w+)(?:\.)(\w+)', r'smtp.\1.\2', email_addr)

    @staticmethod
    def guess_username(email_addr):
        group = re.search('\w+(?=@)', email_addr)

        if group is not None:
            return group.group(0)
        else:
            raise Exception('Can\'t guess email username')


    def attach_files(self, file_paths):
        for file_path in file_paths:
            att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
            att["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            fn = os.path.basename(file_path)
            att["Content-Disposition"] = 'attachment; filename="%s"'%fn
            self.message.attach(att)

    def send(self, receipe, subject, text):
        # Create an instance with attachment
        self.message = MIMEMultipart()
        #self.message['From'] = Header("this a header", 'utf-8')
        #self.message['To'] = Header("测试", 'utf-8')
        self.subject = subject
        self.message['Subject'] = Header(subject, 'utf-8')
        # email plain text
        self.message.attach(MIMEText(text, 'plain', 'utf-8'))

        try:
            smtp_obj = smtplib.SMTP()
            smtp_obj.connect(self.smtp_addr, 25)
            smtp_obj.login(self.username, self.auth_pwd)
            smtp_obj.sendmail(self.email_addr, receipe, self.message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as ex:
            print(ex)
            print("Error: 无法发送邮件")


if __name__ == '__main__':
    email_sender = EmailSender('a19678zy@163.com', 'a88587578')

    email_sender.send(['2053254167@qq.com'],'For test', '只是为了测试')