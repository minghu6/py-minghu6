
(import os re logging logging.handlers smtplib email mimetypes)
(import [email.mime.multipart [MIMEMultipart]]
        [email.message [Message]]
        [email.mime.audio [MIMEAudio]]
        [email.mime.image [MIMEImage]]
        [email.mime.text [MIMEText]]
        [email.mime.base [MIMEBase]]
        [email.mime.application [MIMEApplication]])

(require [minghu6._compat [let]])


(defclass EmailSender []
  (defclass SomeAddrsFailed [Exception])
  (defclass GuessUsernameFailed [Exception])
  (defclass GuessSmtpServerFailed [Exception])

  (defn __init__ [self email-addr auth-pwd &optional [smtp-addr None] [username None] [logger None]]
    (setv self.email-addr email-addr)
    (setv self.auth-pwd auth-pwd)

    ;; First kind of setv method
    (as-> smtp-addr self.smtp-addr
          (cond [(none? self.smtp-addr)
                 (setv self.smtp-addr (emailaddr->smtpserver EmailSender smtp-addr))]))

    ;; Second kind of setv method
    (cond [(none? username) (setv self.username (emailaddr->username EmailSender username))]
          [(setv self.smtp-addr username)])

    (cond [(none? logger) (setv self.logger (.init-default-logger* EmailSender logger))]
          [(setv self.logger logger)]))

  (with-decorator staticmethod
    (defn emailaddr->smtpserver [email-addr]
      (.sub re "(?:.*)@(\w+)(?:\.)(\w+)", r"smtp.\1.\2", email_addr)))

  (with-decorator staticmethod
    (defn emailaddr->username [email-addr]
      (as-> (.search re "\w+(?=@)" email-addr) group
            (cond [(none? group) (raise (GuessUsernameFailed "Can\'t guess email username"))]
                  [(.group group 0)]))))

  (with-decorator staticmethod
    (defn init-default-logger* [logpath &optional [debug False]]
      ;; using as->
      (as-> (.getLogger logging "default_logger") default-logger
            (cond [debug (.setLevel default-logger logging.DEBUG)]
                  [(.setLevel default-logger logging.INFO)])
            (as-> (.Formatter("%(asctime)-15s [%(levelname)s] %(message)s") logging) default-formatter
                  (as-> (.TimedRotatingFileHandler logging.handlers logpath :when "D" :interval 1) trh
                        (.setFormatter trh default-formatter))
                  (as-> (.StreamHandler logging) sh
                        (.setFormatter sh default-formatter))
                  (.addHandler default-logger trh)
                  (.addHandler default-logger sh)
                  (identity default-logger)))))

  (defn send [self receiver extrahds subj bodytext &optional [attaches ()] [bodytext-encoding "utf8"] [tracesize 256]
              (cond [attaches (as-> (Message) msg (.set_payload msg bodytext :charset bodytext-encoding))]
                    [(as-> (MIMEMultipart) msg (.add-attachments* self msg bodytext attaches bodytext-encoding))])
              (let [hdrenc "utf-8"
                    subj (.encode-header* self subj hdrenc)
                    from (.encode-addrheader* self email-addr hdrenc)
                    to (list (map (fn [T] (self.encode-addrheader* T hdrenc)) receiver))
                    tos (.join ", " to)
                    ])
              )
    ;;using let

  )
