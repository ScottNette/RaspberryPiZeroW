from MasterCntrlWrapper import MasterCntrlWrapper
from gpioWrapper import GPIO
import time
import datetime
MstrCntrl = MasterCntrlWrapper()

AllowedTimes = [16, 21]


def main():
    GPIO.add_event_detect(MstrCntrl.gpioCntrl.gpioButton, GPIO.FALLING, callback=buttonISR, bouncetime=2000)
    print('Starting')


    while True: #scheduleCheck():
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
    if len(MstrCntrl.BTCntrl.foundDevice) > 0:
        print('Found!')
        MstrCntrl.MasterSTATE = 'VERIFY'
        MstrCntrl.selectedDevice = MstrCntrl.BTCntrl.foundDevice
        MstrCntrl.BTCntrl.foundDevice = []

    if (MstrCntrl.gpioCntrl.checkOpenButton()):
        MstrCntrl.MasterSTATE = 'UNLOCK'

    if (round(time.time())%10 == 0):
        if (MstrCntrl.gmailCntrl.checkExist('UnlockMaster') ):
        Cond_2 = MstrCntrl.gmailCntrl.checkFrom()
        Cond_3 = MstrCntrl.gmailCntrl.checkTime()
        if (Cond_2 and Cond_3):
            MstrCntrl.MasterSTATE = 'UNLOCK'



def verifyState():
    print('------VERIFY-------')
    print(len(MstrCntrl.selectedDevice))
    print(MstrCntrl.selectedDevice)

    if len(MstrCntrl.selectedDevice) >= 1:
        MstrCntrl.MasterSTATE = 'UNLOCK'
    else:
        MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2], 'Unlock Code?')
        print(MstrCntrl.selectedDevice)
        print(MstrCntrl.MasterSTATE)
        Cond_1 = False
        Cond_2 = False
        Cond_3 = False
        for ii in range(0, 30):
            print('waiting for email')
            Cond_1 = MstrCntrl.gmailCntrl.checkExist('Unlock')
            print(Cond_1)
            if (Cond_1):
                print('Got Cond 1')
                Cond_2 = MstrCntrl.gmailCntrl.checkFrom()
                print(Cond_2)
                Cond_3 = MstrCntrl.gmailCntrl.checkTime()

                print(Cond_3)
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
    print('------UNLOCK-------')
    MstrCntrl.gpioCntrl.openLock()
    MstrCntrl.updateLog()
    if (not  MstrCntrl.buttonISR):
        if (MstrCntrl.masterUnlock):
            print("Unlocked from master code")
            MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2],
                                         'Unlocked by: Master Code')
        else:
            try:
                print(MstrCntrl.selectedDevice)
                print(MstrCntrl.selectedDevice[0][2])
                MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2], 'Unlocked by: '+ MstrCntrl.selectedDevice[0][0])
            except:
                MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2],
                                             'Error finding who unlocked')
    print('waiting')
    startTime = time.time()
    while MstrCntrl.gpioCntrl.checkReed() == MstrCntrl.gpioCntrl.closeDoor:
        if ((time.time() - startTime) > 60):
            break
        time.sleep(0.2)
        #wait

    MstrCntrl.MasterSTATE = 'LOCK'

def lockState():
    print('------LOCK-------')
    print('waiting')
    while MstrCntrl.gpioCntrl.checkReed() == MstrCntrl.gpioCntrl.openDoor:
        pass
        # wait
    #time.sleep(0.5)
    MstrCntrl.gpioCntrl.closeLock()
    MstrCntrl.updateLog()
    if (not MstrCntrl.buttonISR):
        MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2], 'Locked')

    MstrCntrl.selectedDevice = None
    MstrCntrl.buttonISR = False
    #verify lock with pot
    MstrCntrl.MasterSTATE = 'IDLE'
    time.sleep(10)
    print('Back to idle')



def scheduleCheck():
    todayDay = datetime.datetime.today().weekday()
    if (todayDay in [5, 6]):
        return True
    else:
        if ((datetime.datetime.now().hour > AllowedTimes[0]) and (datetime.datetime.now().hour < AllowedTimes[1])):
            return True
        else:
            return False

def buttonISR(channel):
    print("ISR!!")
    time.sleep(0.01)
    if (MstrCntrl.gpioCntrl.checkOpenButton()):
        print("Real!")
        MstrCntrl.buttonISR = True
        MstrCntrl.gpioCntrl.openLock()
        MstrCntrl.MasterSTATE = 'UNLOCK'


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit
        GPIO.cleanup()  # clean up GPIO on normal exit