from GmailWrapper import GmailWrapper
from BTWrapper import BTWrapper
from gpioWrapper import gpioWrapper
from sheetsWrapper import sheetsWrapper
from allowList import *


class MasterCntrlWrapper:


    def __init__(self):
        ## Init Bluetooth
        self.AllowList = externalAllow
        # [['Pretty Name', 'MAC ADDRESS', 'email', 'BT device name'],
        #   ...,
        #   ...]]
        self.AllowListAlt = externalAllowAlt

        #self.CheckList = self.AllowList[0:1]
        self.initCheckList()
        print(self.CheckList)
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

        self.unlockFreeze = False

        self.masterUnlock = False
        self.loopCount = 0
        self.loopCountLED = 0
        self.currTime = 0
        self.prevTime = 0
        self.prevTime2 = 0
        self.doorStatus = True
        self.emailUnlock = False

        self.scheduleSkip = 0
        self.dayDisable = 0
        self.wakeUp = 0
        self.alert = False
        self.timeNow = 0

    def initCheckList(self):
        self.CheckList = self.AllowList[1:3]
        #self.CheckList = self.AllowList[::2]

    def updateLog(self):
        print('Logging')

        try:
            if (self.buttonISR):
                self.logCntrl.updateLog(self.MasterSTATE, "Manual")
            else:
                self.logCntrl.updateLog(self.MasterSTATE, self.selectedDevice[0])
        except:
            print('login error')
            self.logCntrl.login()
            if (self.buttonISR):
                self.logCntrl.updateLog(self.MasterSTATE, "Manual")
            else:
                self.logCntrl.updateLog(self.MasterSTATE, self.selectedDevice[0])




    def gmailLogin(self):
        self.gmailCntrl = GmailWrapper('imap.gmail.com', self.AllowList)

