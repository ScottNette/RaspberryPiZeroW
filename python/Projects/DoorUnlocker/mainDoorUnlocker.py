from MasterCntrlWrapper import MasterCntrlWrapper
import time
MstrCntrl = MasterCntrlWrapper()



def main():

    #init

    MstrCntrl.gpioCntrl.openLock()

    while True:
        if (MstrCntrl.MasterSTATE == 'IDLE'):
            idleState()
        if (MstrCntrl.MasterSTATE == 'VERIFY'):
            verifyState()
        elif (MstrCntrl.MasterSTATE == 'UNLOCK'):
            unlockState()
        elif (MstrCntrl.MasterSTATE == 'LOCK'):
            lockState()


def idleState():

    ### Escape from idle by finding BT device or button push


    print('Looking for Device')
    MstrCntrl.BTCntrl.checkAllow()  #TODO: Change timeout
    if MstrCntrl.BTCntrl.foundDevice[0] != None:
        print('Found!')
        MstrCntrl.MasterSTATE = 'VERIFY'
        MstrCntrl.selectedDevice = MstrCntrl.BTCntrl.foundDevice
        MstrCntrl.BTCntrl.foundDevice = (None, None, None)

    if (MstrCntrl.gpioCntrl.openButton()):
        MstrCntrl.MasterSTATE = 'UNLOCK'



def verifyState():
    if len(MstrCntrl.BTCntrl.foundDevice) >= 2:
        MstrCntrl.MasterSTATE = 'UNLOCK'
    else:
        MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[2], 'Unlock Code?')
        print(MstrCntrl.selectedDevice)
        print(MstrCntrl.MasterSTATE)
        Cond_1 = False
        Cond_2 = False
        Cond_3 = False
        for ii in range(0, 30):
            print('waiting for email')
            Cond_1 = MstrCntrl.gmailCntrl.checkExist()
            print(Cond_1)
            if (Cond_1):
                print('Got Cond 1')
                Cond_2 = MstrCntrl.gmailCntrl.checkFrom()
                Cond_3 = MstrCntrl.gmailCntrl.checkTime()

            if (Cond_1 and Cond_2 and Cond_3):
                print('Got it!')

                Cond_1 = False
                Cond_2 = False
                Cond_3 = False
                MstrCntrl.MasterSTATE = 'UNLOCK'


                break
            else:
                Cond_1 = False
                Cond_2 = False
                Cond_3 = False
                MstrCntrl.MasterSTATE = 'IDLE'

    time.sleep(2)


def unlockState():
    MstrCntrl.gpioCntrl.openLock()
    currentState = MstrCntrl.gpioCntrl.checkReed()
    while MstrCntrl.gpioCntrl.checkReed() == currentState:
        pass
        #wait

    MstrCntrl.MasterSTATE = 'LOCK'

def lockState():
    print('Locking')

    while MstrCntrl.gpioCntrl.checkReed() == MstrCntrl.reedOpen:
        pass
        # wait
    MstrCntrl.gpioCntrl.closeLock()

    #verify lock with pot
    MstrCntrl.MasterSTATE = 'IDLE'



if __name__ == '__main__':
    main()