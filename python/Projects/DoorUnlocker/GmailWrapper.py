from imapclient import IMAPClient, SEEN
import smtplib
import email
import imaplib
from datetime import datetime, timedelta
from pytz import timezone
Arizona = timezone('US/Arizona')

from googleapiclient.discovery import build
#from apiclient import errors

from email.mime.text import MIMEText
from google.oauth2 import service_account
SEEN_FLAG = 'SEEN'
UNSEEN_FLAG = 'UNSEEN'


class GmailWrapper:
    def __init__(self, host,allowlist):
        #   force the user to pass along username and password to log in as
        self.host = host
        self.username = 'sdroid.scott'
        self.password = 'psppsp353'
        self.sender = 'sdroid.scott@gmail.com'
        self.alt = '"Kristen H." <kahorner89@gmail.com>'

        self.message = []
        self.rxSender = None
        self.rxSubject = None
        self.rxDate = None
        self.AllowList = allowlist
        self.AllowListIdx = None
        self.server = None
        self.Selected = None

    def loginIMAP(self):
        try:
            self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
            self.mail.login(self.username, self.password)
            self.mail.select("inbox")  # connect to inbox.
            return True
        except:
            print('IMAP failed login')
            return False



    def checkFrom(self, selectedDevice):
        print(selectedDevice)
        for device in selectedDevice:
            print('checking')
            print(device[2])
            print(self.rxSender)
            print(self.alt)
            if (self.rxSender == device[2] or self.alt == self.rxSender):
                self.Selected = device
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

            if (difftime.total_seconds() < 120):
                return True
            else:
                return False

        except:
            print('error 1')
            pass

        try:
            self.rxDate = self.rxDate.strip(' GMT')
            #print(self.rxDate)
            datetimeEmail = datetime.strptime(self.rxDate, '%a, %d %b %Y %H:%M:%S')
            datetimeNow = datetime.utcnow()
            difftime = datetimeNow - datetimeEmail
            print(difftime)
            if (difftime.total_seconds() < 120):
                return True
            else:
                print('error 2')
                return False

        except:
            pass

        try:
            self.rxDate = self.rxDate[:-4]
            #print(self.rxDate)
            datetimeEmail = datetime.strptime(self.rxDate, '%a, %d %b %Y %H:%M:%S')
            datetimeNow = datetime.utcnow() - timedelta(hours=7)

            difftime = datetimeNow - datetimeEmail
            print(difftime)
            if (difftime.total_seconds() < 120):
                return True
            else:
                print('error 3')
                return False

        except:
            pass

        return False

    def checkExist(self, subject):
        # result, data = self.server.uid('search', 'UNREAD', "ALL")

        #result, data = self.server.search(None, '(UNSEEN)', '(SUBJECT ' + subject + ')')
        result, data = self.mail.search(None, '(UNSEEN)', '(TEXT ' + subject + ')')
        raw_email = []
        # search and return uids instead
        i = len(data[0].split())  # data[0] is a space separate string
        for x in range(i):
            latest_email_uid = data[0].split()[x]  # unique ids wrt label selected
            result, email_data = self.mail.uid('fetch', latest_email_uid, '(RFC822)')
            # fetch the email body (RFC822) for the given ID
            raw_email = email_data[0][1]
            # print(raw_email)


        if(raw_email == []):
            self.mail.check()
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

    def logoutIMAP(self):
        self.mail.logout()

####################################################################################################

    def loginTLS(self):
        for ii in range(5):
            try:
                if self.server == None:
                    self.server = smtplib.SMTP("smtp.gmail.com", 587)
                    self.server.ehlo()
                    self.server.starttls()
                    self.server.ehlo()
                    self.server.login(self.username, self.password)
                    return True

            except:
                print('failed to log in')
                return False



    def sendTxt(self,targets, text):
        self.loginTLS()
        try:
            FROM = self.sender
            TO = targets if isinstance(targets, list) else [targets]
            SUBJECT = 'Unlocker'
            TEXT = text
            # Prepare actual message
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s
                """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

            self.server.sendmail(FROM, TO, message)

            print('successfully sent the mail')
        except:
            print('Failed to send')

        try:
            self.closeConnection()
        except:
            print('Failed to close')



    def closeConnection(self):
        self.server.quit()
        self.server = None


