from GmailWrapper import GmailWrapper
import time
# create an instance of the class, which will also log us in
# the <password> should be the 2-step auth App Password, or your regular password
gmailWrapper = GmailWrapper('imap.gmail.com', 'sdroid.scott', 'ComP353uter~!',None)

#while True:
# search for any unread emails with the subject 'feed cats', and return their Ids
#ids = gmailWrapper.getIdsBySubject('Unlock', unreadOnly=False)
# have the interpreter print the ids variable so you know you've got something

#gmailWrapper.checkFrom()

# now lets mark the email as read
#if ids != []:
 #   gmailWrapper.markAsRead(ids)
 #   print('got it')

Cond_1 = gmailWrapper.checkExist('Unlock')
print(Cond_1)
#print(gmailWrapper.messages)
Cond_2 = gmailWrapper.checkFrom()
print(Cond_2)
Cond_3 = gmailWrapper.checkTime()


gmailWrapper.sendTxt('2038038060@vtext.com','tedddddst')
#d.sendTxt2('test')
#gmailWrapper.sendTxt3('tedddsssssssst')



print('donme')

this = {'SEQ': 47, 'RFC822': 'MIME-Version: 1.0\r\nDate: Mon, 12 Nov 2018 03:00:43 -0700\r\nMessage-ID: <CAM1_sFDc3apxLi9U5Q5H4PVS7-xVrCSBGSUcBOA61rP5qmdFQA@mail.gmail.com>\r\nSubject: Unlock\r\nFrom: Scott Nette <sdroid.scott@gmail.com>\r\nTo: Scott Nette <sdroid.scott@gmail.com>\r\nContent-Type: text/plain; charset="UTF-8"\r\n\r\nUnlock\r\n'}
