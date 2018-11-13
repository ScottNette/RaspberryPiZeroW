from sheetsWrapper import sheetsWrapper
import bluetooth
from bt_proximity import BluetoothRSSI
from GmailWrapper import GmailWrapper
from BTWrapper import BTWrapper
from gpioWrapper import gpioWrapper

import time


class MasterCntrlWrapper:


    def __init__(self):
        ## Init Bluetooth
        self.AllowList = [('Pixel2', '40:4E:36:47:A5:35', '2038038060@vtext.com'),
                     ('Altima', '40:4E:36:47:A5:35', '2038038060@vtext.com')]
        self.RSSIThreshold = (-30, 10)

        self.BTCntrl = BTWrapper(self.AllowList, self.RSSIThreshold)

        ## Gmail init
        self.gmailCntrl = GmailWrapper('imap.gmail.com', 'sdroid.scott', 'ComP353uter~!', self.AllowList)

        self.gpioCntrl = gpioWrapper()

        self.MasterSTATE = 'IDLE'
        self.STATES = ['IDLE', 'UNLOCK', 'LOCK']
        
        self.selectedDevice = None

        self.reedOpen = True
        self.reedClose = False

    def Test(self):
        print('test')

