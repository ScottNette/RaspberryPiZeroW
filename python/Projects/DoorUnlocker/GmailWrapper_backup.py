#!/usr/bin/env python

from imapclient import IMAPClient, SEEN
import smtplib
import email
import imaplib
from datetime import datetime
import time

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
        self.AllowListIdx = None
        self.server = None

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

    def logout(self):
        print('Logging in as ' + self.userName)
        mail = imaplib.IMAP4_SSL('imap.gmail.com')
        # imaplib module implements connection based on IMAPv4 protocol
        try:
            mail.close()
            mail.logout()

            return True
        except:
            raise Exception('Error Logging out')
            return False




    def checkFrom(self, selectedDevice):
        print(selectedDevice)
        for device, address, fromEmail in selectedDevice:
            print(fromEmail)
            print(self.rxSender)
            if (self.rxSender == fromEmail):
                #self.AllowListIdx = index
                return True

        return False

    def getInfo(self):

        # continue inside the same for loop as above
        raw_email_string = self.raw_email.decode('utf-8')
        # converts byte literal to string removing b''
        email_message = email.message_from_string(raw_email_string)

        # print(email_message)
        self.rxSender = email_message.get('From')
        self.rxSubject = email_message.get('Subject')
        self.rxDate = email_message.get('Date')

    def clearInfo(self):
        self.rxSender = None
        self.rxSubject = None
        self.rxDate = None

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
                print('got an email')
                self.getInfo()
                return True
            except:
                return False
           # raise Exception('no email')


    def sendTxt(self,targets, text):
        username = 'sdroid.scott'
        password = 'psppsp353'
        sender = 'sdroid.scott@gmail.com'

        FROM = sender
        TO = targets if isinstance(targets, list) else [targets]
        SUBJECT = 'Unlocker'
        TEXT = text

        # Prepare actual message
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        for ii in range(5):
            Status = self.sendTxtMsg(username, password, FROM, TO, message)
            if Status:
                break
            else:
                print('Trying again')


    def sendTxtMsg(self,username, password, FROM, TO, message):
        try:
            if self.server == None:
                self.server = smtplib.SMTP("smtp.gmail.com", 587)
                self.server.ehlo()
                self.server.starttls()
                self.server.login(username, password)
                self.server.sendmail(FROM, TO, message)
                time.sleep(0.2)
                self.server.close()
                self.server = None

                print('successfully sent the mail')
                return True
        except:
            print('failed to send mail')
            return False

    def closeConnection(self):
        self.server.close()
        self.server = None


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





