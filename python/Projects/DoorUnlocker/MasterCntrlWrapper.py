from GmailWrapper import GmailWrapper
from BTWrapper import BTWrapper
from gpioWrapper import gpioWrapper
from sheetsWrapper import sheetsWrapper


class MasterCntrlWrapper:


    def __init__(self):
        ## Init Bluetooth
        self.AllowList = [('Pixel2', '40:4E:36:47:A5:35', '2038038060@vtext.com'),
                          ('Altima', 'E0:AE:5E:FD:49:26', '2038038060@vtext.com'),
                          ('Kristen', '4C:74:BF:B0:1E:B4', '+16233268643@tmomail.net')]
        self.RSSIThreshold = (-30, 10)

        self.BTCntrl = BTWrapper(self.AllowList, self.RSSIThreshold)

        ## Gmail init
        self.gmailLogin()

        self.gpioCntrl = gpioWrapper()

        self.logCntrl = sheetsWrapper()

        self.timeLock = 0

        self.MasterSTATE = 'IDLE'
        #self.STATES = ['IDLE', 'UNLOCK', 'LOCK']
        
        self.selectedDevice = None

        self.reedOpen = True
        self.reedClose = False
        self.buttonISR = False
        self.reedISR = False

        self.masterUnlock = False
        self.loopCount = 0
        self.loopCountLED = 0
        self.currTime = 0
        self.prevTime = 0
        self.prevTime2 = 0
        self.doorStatus = True

    def Test(self):
        print('test')

    def updateLog(self):
        print('Logging')

        try:
            if (self.buttonISR):
                self.logCntrl.updateLog(self.MasterSTATE, "Manual")
            else:
                self.logCntrl.updateLog(self.MasterSTATE, self.selectedDevice[0][0])
        except:
            print('login error')
            self.logCntrl.login()
            if (self.buttonISR):
                self.logCntrl.updateLog(self.MasterSTATE, "Manual")
            else:
                self.logCntrl.updateLog(self.MasterSTATE, self.selectedDevice[0][0])




    def gmailLogin(self):
        self.gmailCntrl = GmailWrapper('imap.gmail.com', 'sdroid.scott', 'ComP353uter~!', self.AllowList)

