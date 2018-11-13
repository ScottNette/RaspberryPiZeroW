#!/usr/bin/env python

from imapclient import IMAPClient, SEEN
import smtplib
import email

from googleapiclient.discovery import build
from apiclient import errors

from email.mime.text import MIMEText
from google.oauth2 import service_account
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
        self.rxSender = None
        self.rxSubject = None
        self.rxDate = None

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

    def getFrom(self):
        uid, message_data = self.server.fetch(self.messages, 'RFC822').items()
        email_message = email.message_from_bytes(message_data[b'RFC822'])
        self.rxSender = email_message.get('From')
        self.rxSubject = email_message.get('Subject')
        self.rxDate = email_message.get('Date')




    def markAsRead(self, mailIds, folder='INBOX'):
        self.setFolder(folder)
        self.server.set_flags(mailIds, [SEEN])

    def setFolder(self, folder):
        self.server.select_folder(folder)

    def sendTxt(self,text):

        username = 'sdroid.scott'
        password = 'ComP353uter~!'
        sender = 'sdroid.scott@gmail.com'
        targets = '2038038060@vtext.com'

        #msg = MIMEMultipart()
        msg = MIMEText(text)
        msg['Subject'] = 'Unlocker'
        msg['From'] = sender
        msg['To'] = targets

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        #server = smtplib.SMTP_SSL('smtp.gmail.com', 587)
        server.login(username, password)
        #server.sendmail(sender, targets, msg.as_string())
        server.send_message(msg)
        server.quit()
        print(msg)

    def sendTxt2(self,text):
        username = 'sdroid.scott'
        password = 'ComP353uter~!'
        sender = 'sdroid.scott@gmail.com'
        targets = '2038038060@vtext.com'

        # SMTP_SSL Example
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()  # optional, called by login()
        server_ssl.login(username, password)
        # ssl server doesn't support or need tls, so don't call server_ssl.starttls()
        server_ssl.sendmail(sender, targets, text)
        # server_ssl.quit()
        server_ssl.close()
        print
        'successfully sent the mail'

    def sendTxt3(self,text):
        username = 'sdroid.scott'
        password = 'ComP353uter~!'
        sender = 'sdroid.scott@gmail.com'
        targets = '2038038060@vtext.com'

        FROM = sender
        TO = targets if isinstance(targets, list) else [targets]
        SUBJECT = 'Unlocker'
        TEXT = text

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        print(message)
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(username, password)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent the mail')
        except:
            print('failed to send mail')


    def create_message(self, sender, to, subject, message_text):
        """Create a message for an email.
        Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
        Returns:
          An object containing a base64url encoded email object.
        """
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': str(message)}

    def send_message(self,service, user_id, message):
        """Send an email message.
        Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.
        Returns:
          Sent Message.
        """
        try:
            message = (service.users().messages().send(userId=user_id, body=message)
                       .execute())
            print('Message Id: %s' % message['id'])
            return message
        except errors.HttpError as error:
            print('An error occurred: %s' % error)

    def service_account_login(self):
        SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/gmail.metadata']
        SERVICE_ACCOUNT_FILE = 'client_secret.json'

        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        delegated_credentials = credentials.with_subject('sdroid.scott@gmail.com')
        service = build('gmail', 'v1', credentials=delegated_credentials)
        return service





