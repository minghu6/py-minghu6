
(import os re logging logging.handler smtplib email mimetypes)
(import [email.mime.multipart [MIMEMultipart]]
        [email.mime.message [Message]]
        [email.mime.audio [MIMEAudio]]
        [email.mime.image [MIMEImage]]
        [email.mime.text [MIMEText]]
        [email.mime.base [MIMEBase]]
        [email.mime.application [MIMEApplication]])

(defclass EmailSender []
  (defclass SomeAddrsFailed [Exception])

  (defn __init__ [self email-addr auth-pwd &optional [smtp-addr None] [username None] [logger None]]
    (setv self.email-addr email-addr)
    (setv self.auth-pwd auth-pwd)

    ))
