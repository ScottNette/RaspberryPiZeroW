#!/usr/bin/env python

from imapclient import IMAPClient, SEEN
import smtplib
import email
import imaplib
from datetime import datetime

from googleapiclient.discovery import build
from apiclient import errors

from email.mime.text import MIMEText
from google.oauth2 import service_account
SEEN_FLAG = 'SEEN'
UNSEEN_FLAG = 'UNSEEN'


class GmailWrapper:
    def __init__(self, host, userName, password,allowlist):
        #   force the user to pass along username and password to log in as
        self.host = host
        self.userName = userName
        self.password = password
        self.login()
        self.message = []
        self.rxSender = None
        self.rxSubject = None
        self.rxDate = None
        self.AllowList = allowlist

    def login(self):
        print('Logging in as ' + self.userName)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        # imaplib module implements connection based on IMAPv4 protocol
        try:
            mail.login(self.userName, self.password)

            mail.list()  # Lists all labels in GMail
            mail.select('inbox')  # Connected to inbox.
            self.server = mail
            return True
        except:
            raise Exception('Error Logging In')
            return False





    def checkFrom(self):


        # continue inside the same for loop as above
        raw_email_string = self.raw_email.decode('utf-8')
        # converts byte literal to string removing b''
        email_message = email.message_from_string(raw_email_string)

        #print(email_message)
        self.rxSender = email_message.get('From')
        self.rxSubject = email_message.get('Subject')
        self.rxDate = email_message.get('Date')


        for device, address, fromEmail in self.AllowList:
            print(fromEmail)
            print(self.rxSender)
            if (self.rxSender == fromEmail):
                return True

        return False

    def checkTime(self):
        try:
            self.rxDate = self.rxDate.strip(' +0000')
            print(self.rxDate)
            datetimeEmail = datetime.strptime(self.rxDate, '%d %b %Y %H:%M:%S')
            datetimeNow = datetime.utcnow()
            difftime = datetimeNow - datetimeEmail
            print(difftime)
            if (difftime.total_seconds() < 60):
                return True
            else:
                return False

        except:
            pass



        try:
            self.rxDate = self.rxDate.strip(' GMT')
            print(self.rxDate)
            datetimeEmail = datetime.strptime(self.rxDate, '%a, %d %b %Y %H:%M:%S')
            datetimeNow = datetime.utcnow()
            difftime = datetimeNow - datetimeEmail
            print(difftime)
            if (difftime.total_seconds() < 60):
                return True
            else:
                return False

        except:
            pass




        return False



    def checkExist(self, subject):
        # result, data = self.server.uid('search', 'UNREAD', "ALL")
        #result, data = self.server.search(None, '(UNSEEN)', '(SUBJECT ' + subject + ')')
        result, data = self.server.search(None, '(UNSEEN)', '(TEXT ' + subject + ')')
        #print(data)
        raw_email = []
        # search and return uids instead
        i = len(data[0].split())  # data[0] is a space separate string
        for x in range(i):
            latest_email_uid = data[0].split()[x]  # unique ids wrt label selected
            result, email_data = self.server.uid('fetch', latest_email_uid, '(RFC822)')
            # fetch the email body (RFC822) for the given ID
            raw_email = email_data[0][1]
            # print(raw_email)


        if(raw_email == []):
            self.server.check()
            return False
        else:
            try:
                self.raw_email = raw_email
                print('got an rmail')
                return True
            except:
                return False
           # raise Exception('no email')


    def sendTxt(self,targets, text):
        username = 'sdroid.scott'
        password = 'ComP353uter~!'
        sender = 'sdroid.scott@gmail.com'

        FROM = sender
        TO = targets if isinstance(targets, list) else [targets]
        SUBJECT = 'Unlocker'
        TEXT = text

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

        #print(message)
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
            #print('Message Id: %s' % message['id'])
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





