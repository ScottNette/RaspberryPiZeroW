#!/usr/bin/env python
import email
from imapclient import IMAPClient, SEEN
import smtplib
from email.mime.text import MIMEText

SEEN_FLAG = 'SEEN'
UNSEEN_FLAG = 'UNSEEN'


class GmailWrapper:
    def __init__(self, host, userName, password):
        #   force the user to pass along username and password to log in as
        self.host = host
        self.userName = userName
        self.password = password
        self.login()
        self.message = []

    def login(self):
        print('Logging in as ' + self.userName)
        server = IMAPClient(self.host, use_uid=True, ssl=True)
        server.login(self.userName, self.password)
        self.server = server

    #   The IMAPClient search returns a list of Id's that match the given criteria.
    #   An Id in this case identifies a specific email
    def getIdsBySubject(self, subject, unreadOnly=True, folder='INBOX'):
        #   search within the specified folder, e.g. Inbox
        self.server.select_folder(folder, readonly=True)

        #   build the search criteria (e.g. unread emails with the given subject)
        self.searchCriteria = ['SUBJECT', subject, UNSEEN_FLAG]


        if (unreadOnly == False):
            #   force the search to include "read" emails too
            self.searchCriteria.append(SEEN_FLAG)

        self.messages = self.server.search('UNSEEN')
        #   conduct the search and return the resulting Ids
        return self.messages



    def markAsRead(self, mailIds, folder='INBOX'):
        self.setFolder(folder)
        self.server.set_flags(mailIds, [SEEN])

    def setFolder(self, folder):
        self.server.select_folder(folder)

    def sendTxt(self,text):
        smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
        smtp_ssl_port = 465
        username = 'sdroid,scott@gmail.com'
        password = 'ComP353uter~!'
        sender = 'sdroid,scott@gmail.com'
        targets = ['2038038060@vtext.com']

        msg = MIMEText(text)
        msg['Subject'] = 'Unlocker'
        msg['From'] = sender
        msg['To'] = ', '.join(targets)

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(sender, targets, msg.as_string())
        server.quit()