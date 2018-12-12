from MasterCntrlWrapper import MasterCntrlWrapper
from gpioWrapper import GPIO
import time
import datetime
MstrCntrl = MasterCntrlWrapper()

AllowedTimes = [16, 21]


def main():
    GPIO.add_event_detect(MstrCntrl.gpioCntrl.gpioButton, GPIO.FALLING, callback=buttonISR, bouncetime=6000)
    GPIO.add_event_detect(MstrCntrl.gpioCntrl.gpioReed, GPIO.FALLING, callback=reedISR, bouncetime=6000)
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

    if (round(time.time()) != MstrCntrl.currTime):
        MstrCntrl.currTime = round(time.time())

        ########## BT Scan Control
        if (MstrCntrl.currTime % 9 == 0):
            # 2 min Timeout after an unlock
            if (time.time() - MstrCntrl.timeLock > 120):
                print('Looking for Device')
                print('Delta Tscan = ' + str(round(time.time()) - MstrCntrl.prevTime))

                MstrCntrl.BTCntrl.checkAllow()
                print('Delta Tdone = ' + str(round(time.time()) - MstrCntrl.currTime))

                MstrCntrl.prevTime = MstrCntrl.currTime
                if len(MstrCntrl.BTCntrl.foundDevice) > 0:
                    print('Found!')
                    MstrCntrl.MasterSTATE = 'VERIFY'
                    MstrCntrl.selectedDevice = MstrCntrl.BTCntrl.foundDevice
                    MstrCntrl.BTCntrl.foundDevice = []


            ########## GMail check
            MstrCntrl.loopCount += 1
            if (MstrCntrl.loopCount >= 1):
                print('Delta Tgmail = ' + str(MstrCntrl.currTime - MstrCntrl.prevTime2))
                MstrCntrl.prevTime2 = MstrCntrl.currTime
                Cond_2 = False
                Cond_3 = False

                if (MstrCntrl.gmailCntrl.checkExist('UnlockMaster') ):
                    Cond_2 = MstrCntrl.gmailCntrl.checkFrom()
                    Cond_3 = MstrCntrl.gmailCntrl.checkTime()
                    if (Cond_2):
                        MstrCntrl.masterUnlock = True
                        MstrCntrl.MasterSTATE = 'UNLOCK'

                if (MstrCntrl.gmailCntrl.checkExist('RelayOff')):
                    MstrCntrl.gpioCntrl.RelayOff()

                if (MstrCntrl.gmailCntrl.checkExist('Lock')):
                    MstrCntrl.gpioCntrl.closeLock()

                if (MstrCntrl.gmailCntrl.checkExist('Status')):
                    if (MstrCntrl.gpioCntrl.checkReed()):
                        temp = 'Closed'
                    else:
                        temp = 'Opened'
                    MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2], 'Current State:' + MstrCntrl.MasterSTATE +', Door is: ' + str(temp))

                MstrCntrl.loopCount = 0


        ########## LED Control
        if (MstrCntrl.currTime % 2 == 0):
            MstrCntrl.loopCountLED +=1
            if ( MstrCntrl.loopCountLED == 1):
                print('LED ON')
                MstrCntrl.gpioCntrl.LEDOn()
            else:
                print('LED OFF')
                MstrCntrl.gpioCntrl.LEDOff()
                MstrCntrl.loopCountLED = 0

        if (MstrCntrl.reedISR and (not MstrCntrl.gpioCntrl.openDoor) and (not MstrCntrl.buttonISR) and (MstrCntrl.MasterSTATE == 'IDLE')):
            MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2], 'Break in!!!!!!!!!')



def verifyState():
    print('------VERIFY-------')
    print(MstrCntrl.selectedDevice)

    if len(MstrCntrl.selectedDevice) >= 2:
        MstrCntrl.MasterSTATE = 'UNLOCK'
    else:
        ### Request unlocker code
        MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2], 'Unlock Code?')
        Cond_1 = False
        Cond_2 = False
        Cond_3 = False

        for ii in range(0, 30):
            print('waiting for email')
            Cond_1 = MstrCntrl.gmailCntrl.checkExist('Unlock')
            if (Cond_1):
                Cond_2 = MstrCntrl.gmailCntrl.checkFrom()
                Cond_3 = MstrCntrl.gmailCntrl.checkTime()

            if (Cond_1 and Cond_2 and Cond_3):
                print('Got it!')
                MstrCntrl.MasterSTATE = 'UNLOCK'
                break
            else:
                MstrCntrl.MasterSTATE = 'IDLE'

            time.sleep(2)


def unlockState():
    print('------UNLOCK-------')

    if (not MstrCntrl.buttonISR):
        print('not ISR')
        MstrCntrl.gpioCntrl.openLock()
        MstrCntrl.doorStatus = MstrCntrl.gpioCntrl.checkReed()

        if (MstrCntrl.masterUnlock):
            print("Unlocked from master code")
            MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2],'Unlocked by: Master Code')
            MstrCntrl.selectedDevice[0][2] = 'Master Code'
        else:
            try:
                MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2], 'Unlocked by: '+ MstrCntrl.selectedDevice[0][0])
            except:
                MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2], 'Error finding who unlocked')
        print('waiting')

    else:
        print('unlock ISR')

    #Capture door event
    startTime = time.time()
    while (MstrCntrl.doorStatus == MstrCntrl.gpioCntrl.closeDoor):
        MstrCntrl.doorStatus = MstrCntrl.gpioCntrl.checkReed()
        if ((time.time() - startTime) > 60):
            print('Unlock timeout')
            break
        time.sleep(0.2)

    MstrCntrl.reedISR = False
    MstrCntrl.updateLog()
    MstrCntrl.MasterSTATE = 'LOCK'


def lockState():
    print('------LOCK-------')

    # Wait for action
    while MstrCntrl.doorStatus == MstrCntrl.gpioCntrl.openDoor:
        MstrCntrl.doorStatus = MstrCntrl.gpioCntrl.checkReed()
        pass

    MstrCntrl.gpioCntrl.closeLock()
    MstrCntrl.updateLog()

    if (not MstrCntrl.buttonISR):
        MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[0][2], 'Locked')

    MstrCntrl.selectedDevice = None
    MstrCntrl.buttonISR = False
    MstrCntrl.MasterSTATE = 'IDLE'
    MstrCntrl.timeLock = time.time()
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


###############  ISR Definitions ##############
def buttonISR(channel):
    print("button ISR!!")
    time.sleep(0.01)

    if (MstrCntrl.gpioCntrl.checkOpenButton() and (not MstrCntrl.buttonISR)):
        print("Real butten!")
        MstrCntrl.buttonISR = True
        MstrCntrl.MasterSTATE = 'UNLOCK'
        MstrCntrl.gpioCntrl.openLock()

def reedISR(channel):
    print("reed ISR!!")
    time.sleep(0.01)
    if ((not MstrCntrl.gpioCntrl.checkReed()) and (not MstrCntrl.reedISR)):
        print("Real reed!")
        MstrCntrl.reedISR = True
        MstrCntrl.doorStatus = MstrCntrl.gpioCntrl.openDoor


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        GPIO.cleanup()  # clean up GPIO on CTRL+C exit
        print('Cleaned')
    GPIO.cleanup()  # clean up GPIO on normal exit
    print('Cleaned')