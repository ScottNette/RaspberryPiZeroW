from GmailWrapper import GmailWrapper
import time
# create an instance of the class, which will also log us in
# the <password> should be the 2-step auth App Password, or your regular password
#gmailWrapper = GmailWrapper('imap.gmail.com', 'sdroid.scott', 'ComP353uter~!')

#while True:
# search for any unread emails with the subject 'feed cats', and return their Ids
#ids = gmailWrapper.getIdsBySubject('Test2', unreadOnly=False)
# have the interpreter print the ids variable so you know you've got something
# now lets mark the email as read
#if ids != []:
#    gmailWrapper.markAsRead(ids)
 #   print('got it')

#time.sleep(0.5)

EMAIL_FROM = 'sdroid.scott@gmail.com'
EMAIL_TO = 'mark.kjkljlkjkl@facebook.com'
EMAIL_SUBJECT = 'Hello  from Lyfepedia!'
EMAIL_CONTENT = 'Hello, this is a test\nLyfepedia\nhttps://lyfepedia.com'

d = GmailWrapper

service = d.service_account_login()
# Call the Gmail API
message = d.create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
#sent = d.send_message(service,'sdroid.scott@gmail.com', message)

d.sendTxt('tedddddst')
#d.sendTxt2('test')
#d.sendTxt3('tedddsssssssst')



print('donme')