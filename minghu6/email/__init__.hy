
(import os re logging logging.handlers smtplib email mimetypes)
(import [email.mime.multipart [MIMEMultipart]]
        [email.message [Message]]
        [email.mime.audio [MIMEAudio]]
        [email.mime.image [MIMEImage]]
        [email.mime.text [MIMEText]]
        [email.mime.base [MIMEBase]]
        [email.mime.application [MIMEApplication]])

(require [hy.contrib.walk [let]])


(defclass EmailSender []
  (defclass SomeAddrsFailed [Exception])
  (defclass GuessUsernameFailed [Exception])
  (defclass GuessSmtpServerFailed [Exception])

  (defn __init__ [self email-addr auth-pwd &optional [smtp-server None] [username None]
                  [logger None] [logpath "email-sender.log"] [debug False]]
    (setv self.email-addr email-addr)
    (setv self.auth-pwd auth-pwd)

    (cond [(none? smtp-server) (setv self.smtp-server (.emailaddr->smtpserver EmailSender self.email-addr))]
          [(setv self.smtp-server smtp-server)])

    (cond [(none? username) (setv self.username (.emailaddr->username EmailSender self.email-addr))]
          [(setv self.username username)])

    (cond [(none? logger) (setv self.logger (.init-default-logger* EmailSender logpath debug))]
          [(setv self.logger logger)]))

  (with-decorator staticmethod
    (defn emailaddr->smtpserver [email-addr]
      (.sub re "(?:.*)@(\w+)(?:\.)(\w+)" r"smtp.\1.\2" email-addr)))

  (with-decorator staticmethod
    (defn emailaddr->username [email-addr]
      (let [group (.search re "\w+(?=@)" email-addr)]
           (cond [(none? group) (raise (.GuessUsernameFailed EmailSender "Can\'t guess email username"))])
           (.group group 0))))

  (with-decorator staticmethod
    (defn init-default-logger* [logpath &optional [debug True]]
      ;; using as->
      (let [default-logger (.getLogger logging "default_logger")]
            (cond [debug (.setLevel default-logger logging.DEBUG)]
                  [(.setLevel default-logger logging.INFO)])
            (let [default-formatter (.Formatter logging  "%(asctime)-15s [%(levelname)s] %(message)s")]
                  (let [trh (.TimedRotatingFileHandler logging.handlers logpath :when "D" :interval 1)]
                       (.setFormatter trh default-formatter)
                       (.addHandler default-logger trh))
                  (let [sh (.StreamHandler logging)]
                       (.setFormatter sh default-formatter)
                       (.addHandler default-logger sh)))
            default-logger)))

  (defn create-plaintext-msg* [self bodytext bodytext-encoding]
    (setv msg (Message))
    (.set_payload msg bodytext :charset bodytext-encoding)
    (return msg))

  (defn create-attachments-msg* [self bodytext attachments bodytext-encoding]
    (setv msg (MIMEMultipart))
    (.add-attachments* self msg bodytext attachments bodytext-encoding)
    (return msg))

  (defn send [self receiver extrahds subj bodytext &optional [attaches ()] [bodytext-encoding "utf8"] [tracesize 256]]
    (cond [(not attaches)
           (setv msg (.create-plaintext-msg* self bodytext bodytext-encoding))]
          [(setv msg (.create-attachments-msg* self bodytext attaches bodytext-encoding))])
    (let [subj subj
          from self.email-addr
          to receiver
          tos (.join ", " to)
          recip to]
         (assoc msg "From" from "To" tos "Subject" subj "Date" (.formatdate email.utils))
         (for [[name* value] extrahds]
           (cond [value
                  (cond [(not (in (.lower name*) ["cc" "bcc"]))
                         (assoc msg name* value)]
                        [(.append recip value) None])]))


         (let [recip (list (set recip))
               full-text (.as_string msg)]
              (.info self.logger (+ "Sending to... " (.join ";" recip)))
              (.info self.logger (.join "" (take tracesize full-text)))
              (let [server (.SMTP smtplib self.smtp-server)]
                   (.connect server self.smtp-server)
                   (.login server self.username self.auth-pwd)
                   (try
                     (setv failed (.sendmail server from recip full-text))
                     (except (.close server) (raise))
                     (else (.quit server)))
                   (cond [failed (let [err-msg (% "Failed addr: %s\n" failed)]
                                      (.error self.logger err-msg)
                                      (raise (.SomeAddrsFailed EmailSender err-msg)))]))
              (.info self.logger "Send exit."))))

  (defn encode-header* [self headertext &optional [unicode-encoding "utf-8"]]
                        (try
                          (.encode headertext "ascii")
                          (except [] (try
                                    (.encode (.make_header email.header [(tuple [headertext unicode-encoding])]))
                                    (except [])))))

  (defn encode-addrheader* [self headertext &optional [unicode-encoding "utf-8"]]
    (try
      (let [pairs (.getaddresses email.util [headertext]) encoded []]
           (for [[name* addr] pairs]
             (try
               (.encode name* "ascii")
               (except [UnicodeError]
                 (try
                   (setv name* (.encode (.make_header email.header [(tuple
                                                                      (.encode name* unicode-encoding) unicode-encoding)])))
                   (except [] (setv name* None)))))
             (.append encoded (.formataddr email.utils (tuple [name* addr]))))
           (let [fullhdr (.join ", " encoded)]
                (cond [(or (> (len fullhdr) 72) (in "\n" fullhdr))
                       (setv fullhdr (.join ",\n " encoded))])
                       fullhdr))
      (except [] (.encode-header* self headertext))))

  (defn add-attachments* [self mainmsg bodytext attaches bodytext-encoding]
    (let [msg (MIMEText bodytext :_charset bodytext-encoding)]
         (.attach mainmsg msg)
         (for [filename attaches]
           (cond [(not (.isfile os.path filename)) (continue)])
           (let [tar (.guess_type mimetypes filename) contype (first tar) encoding (last tar)]
                (cond [(or (none? contype) (not (none? encoding))) (setv contype "application/octet-stream")])
                (.debug self.logger (+ "Adding" contype))
                (let [tar (.split contype "/" 1) maintype (first tar) subtype (last tar)]
                     (cond [(= "text" maintype)
                            (with [data (open filename "r" :encoding "utf-8")]
                              (setv msg (MIMEText (.read data) :_subtype subtype)))]
                           [(cond [(= "image")
                                   (with [data (open filename "rb")]
                                     (setv msg (MIMEImage (.read data) :_subtype subtype)))]
                                  [(cond [(= "audio")
                                          (with [data (open filename "rb")]
                                            (setv msg (MIMEAudio (.read data) :_subtype subtype)))]
                                         [(cond [(= "application")
                                                   (with [data (open filename "rb")]
                                                     (setv msg (MIMEApplication (.read data) :_subtype subtype)))]
                                                [(with [data (open filename "rb")]
                                                   (setv msg (MIMEBase maintype subtype))
                                                   (.set_payload (.read data)))])])])])))
             (.debug self.logger (% "add attachment %s" filename))
           (let [basename (.basename os.path filename)]
                (.add_header msg "Content-Disposition" "attachment" :filename basename)
                (.attach mainmsg msg)))

         (setv mainmsg.preamble "A multi-part MIME format message.\n")
         (setv mainmsg.epilogue ""))))
