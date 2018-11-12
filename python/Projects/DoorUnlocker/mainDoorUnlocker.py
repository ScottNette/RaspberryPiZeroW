from sheetsWrapper import sheetsWrapper
import bluetooth
from bt_proximity import BluetoothRSSI
from GmailWrapper import GmailWrapper
import time

MasterSTATE = 'IDLE'
STATES = ['IDLE','UNLOCK','LOCK']


def main():
    while True:
        if ( MasterSTATE == 'IDLE'):
            idleState()
        elif ( MasterSTATE == 'UNLOCK'):
            unlockState()
        elif (MasterSTATE == 'LOCK'):
            lockState()

        time.sleep(2)


def idleState():



def unlockState():



def lockState():


