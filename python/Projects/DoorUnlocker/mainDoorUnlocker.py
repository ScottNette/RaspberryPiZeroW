from MasterCntrlWrapper import MasterCntrlWrapper
from gpioWrapper import GPIO
import time
import datetime
from pytz import timezone
MstrCntrl = MasterCntrlWrapper()

AllowedTimes = [17, 22]
Arizona = timezone('US/Arizona')


def main():
    GPIO.add_event_detect(MstrCntrl.gpioCntrl.gpioButton, GPIO.FALLING, callback=buttonISR, bouncetime=6000)
    GPIO.add_event_detect(MstrCntrl.gpioCntrl.gpioReed, GPIO.FALLING, callback=reedISR, bouncetime=6000)
    MstrCntrl.unlockFreeze = False
    print('Starting')
    MstrCntrl.gpioCntrl.LEDOff()


    while True:

        scheduleCheck()

        if (MstrCntrl.MasterSTATE == 'IDLE'):
            idleState()

        if (MstrCntrl.MasterSTATE == 'VERIFY'):
            verifyState()

        if (MstrCntrl.MasterSTATE == 'UNLOCK'):
            unlockState()

        if (MstrCntrl.MasterSTATE == 'LOCK'):
            lockState()

        if (MstrCntrl.MasterSTATE == 'SLEEP'):
            sleepState()



def sleepState():

    if ((MstrCntrl.loopCount % 10) == 0):
        gmailCheck()


def idleState():

    ########## BT Scan Control
    if (not MstrCntrl.buttonISR):
        if (MstrCntrl.loopCount % 5 == 0):
            # 2 min Timeout after an unlock
            if (time.time() - MstrCntrl.timeLock > 120):
                print('Looking for Device')
                MstrCntrl.BTCntrl.checkAllow()

                MstrCntrl.prevTime = round(time.time())
                if len(MstrCntrl.BTCntrl.foundDevice) > 0:
                    MstrCntrl.MasterSTATE = 'VERIFY'
                    MstrCntrl.selectedDevice = MstrCntrl.BTCntrl.foundDevice
                    MstrCntrl.BTCntrl.foundDevice = []
                    print(MstrCntrl.selectedDevice[0])
                    print('Found: ' + MstrCntrl.selectedDevice[0])


            ########## GMail check
            if ((MstrCntrl.loopCount % 10) == 0):
                gmailCheck()


            ########## LED Control
            if ((MstrCntrl.loopCount % 2) == 0):
                MstrCntrl.loopCountLED +=1
                if ( MstrCntrl.loopCountLED == 1):
                    MstrCntrl.gpioCntrl.LEDOn()
                else:
                    MstrCntrl.gpioCntrl.LEDOff()
                    MstrCntrl.loopCountLED = 0

            if ((MstrCntrl.doorStatus == MstrCntrl.gpioCntrl.openDoor) and not MstrCntrl.alert and not MstrCntrl.unlockFreeze):
                MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2], 'Break in!!!!!!!!!')
                MstrCntrl.alert = True

             #   while (True):
             #       pass



def verifyState():
    print('------VERIFY-------')
    print(MstrCntrl.selectedDevice)
    MstrCntrl.scheduleSkip = 0


    #Found Altima, Check Pixel or got email, check pixel
    if ((MstrCntrl.selectedDevice == MstrCntrl.AllowList[1]) or (MstrCntrl.emailUnlock == True) ):
        print('got email?')
        for ii in range(0, 3):
            if (MstrCntrl.emailUnlock):
                MstrCntrl.BTCntrl.checkSingle(MstrCntrl.selectedDevice)
            else:
                MstrCntrl.BTCntrl.checkSingle(MstrCntrl.AllowList[0])

            print(MstrCntrl.BTCntrl.foundDevice)
            #print(MstrCntrl.AllowList[0])
            if (MstrCntrl.BTCntrl.foundDevice == MstrCntrl.AllowList[0]):
                MstrCntrl.MasterSTATE = 'UNLOCK'
                break
            else:
                print('------IDLE-------')
                MstrCntrl.MasterSTATE = 'IDLE'

    else:
        print('found BT')

        Cond_1 = False
        Cond_2 = False
        Cond_3 = False
        #print(MstrCntrl.selectedDevice[2])
        MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.selectedDevice[2], 'Unlock code?')
        for ii in range(0, 30):
            #print('waiting for email')
            MstrCntrl.gmailCntrl.loginIMAP()
            Cond_1 = MstrCntrl.gmailCntrl.checkExist('Unlock')
            MstrCntrl.gmailCntrl.logoutIMAP()
            if (Cond_1):
                Cond_2 = MstrCntrl.gmailCntrl.checkFrom([MstrCntrl.selectedDevice])
                print(MstrCntrl.gmailCntrl.rxSender)
                print(MstrCntrl.selectedDevice)
                Cond_3 = MstrCntrl.gmailCntrl.checkTime()
                print('cond Check')
                print(Cond_2)
                print(Cond_3)
            if (Cond_1 and Cond_2 and Cond_3):
                print('Got it!')
                MstrCntrl.gmailCntrl.clearInfo()
                MstrCntrl.MasterSTATE = 'UNLOCK'

                MstrCntrl.CheckList.remove(MstrCntrl.selectedDevice)
                MstrCntrl.dayDisable = datetime.datetime.today().day

                break
            else:
                MstrCntrl.MasterSTATE = 'IDLE'
                MstrCntrl.selectedDevice = None

            time.sleep(2)


def unlockState():
    print('------UNLOCK-------')

    if (not MstrCntrl.buttonISR):
        print('in not ISR')
        MstrCntrl.gpioCntrl.openLock()
        #MstrCntrl.doorStatus = MstrCntrl.gpioCntrl.checkReed()


        if (MstrCntrl.masterUnlock):
            print("Unlocked from master code")
            MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2],'Unlocked by: Master Code')
            MstrCntrl.selectedDevice = MstrCntrl.AllowList[0]
            MstrCntrl.selectedDevice[0] = 'Master Code'
        else:
            try:
                MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2], 'Unlocked by: '+ MstrCntrl.selectedDevice[0] +'\n Time: ' + MstrCntrl.timeNow )
            except:
                MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2], 'Error finding who unlocked')
        #print('waiting')

    else:
        print('unlock ISR')

    #Capture door event
    startTime = time.time()
    oneTime = True
    while (MstrCntrl.doorStatus == MstrCntrl.gpioCntrl.closeDoor):
        if oneTime:
            MstrCntrl.updateLog()
            oneTime = False
        MstrCntrl.doorStatus = MstrCntrl.gpioCntrl.checkReed()
        if ((time.time() - startTime) > 60):
            print('Unlock timeout')
            break
        time.sleep(0.2)

    MstrCntrl.reedISR = False

    if (MstrCntrl.unlockFreeze):
        MstrCntrl.buttonISR = False
        print('Frozen')
        while MstrCntrl.unlockFreeze:
            time.sleep(1)

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
        MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2], 'Locked at:' + MstrCntrl.timeNow)
       # MstrCntrl.gmailCntrl.closeConnection

    MstrCntrl.selectedDevice = None
    MstrCntrl.buttonISR = False
    MstrCntrl.MasterSTATE = 'IDLE'
    MstrCntrl.scheduleSkip = 0
    MstrCntrl.emailUnlock = False
    MstrCntrl.timeLock = time.time()
    MstrCntrl.initCheckList()
    print('Back to idle')



def scheduleCheck():


    if (round(time.time()) != MstrCntrl.currTime):
        MstrCntrl.currTime = round(time.time())

        MstrCntrl.timeNow = str(datetime.datetime.time(datetime.datetime.now(Arizona)).replace(microsecond=0))
        todayDay = datetime.datetime.today().weekday()
        hourNow = datetime.datetime.time(datetime.datetime.now(Arizona)).hour

        if (MstrCntrl.loopCount == 1000):
            MstrCntrl.loopCount = 0


        if ((MstrCntrl.loopCount % 50) == 0):
            print ('hour: ' + str(hourNow))
            print("sched skip = " + str(MstrCntrl.scheduleSkip))
            print("hour check = " + str((todayDay in [5, 6]) or ((hourNow >= AllowedTimes[0]) and (hourNow <= AllowedTimes[1])) ))
            print("current Hour: " +  str(hourNow))
            print ('day: ' + str(todayDay))
            print('sked skip: ' + str(MstrCntrl.scheduleSkip))
            print(MstrCntrl.MasterSTATE)

        MstrCntrl.loopCount += 1



        if MstrCntrl.scheduleSkip == 1:
        #    if ((MstrCntrl.loopCount % 10) == 10):
            print('skip sked')
            return True

        else:
            # if weekend or in allowed times
            if ((todayDay in [4, 5, 6]) or ((hourNow >= AllowedTimes[0]) and (hourNow <= AllowedTimes[1])) ):
                # New day refresh
                if (MstrCntrl.wakeUp == 0):
                    MstrCntrl.initCheckList()
                    MstrCntrl.wakeUp = 1
                    MstrCntrl.alert = False
                    MstrCntrl.MasterSTATE = 'IDLE'
                return True
            else:
                MstrCntrl.wakeUp = 0
                MstrCntrl.MasterSTATE = 'SLEEP'
                return False





def gmailCheck():
    #print('Delta Tgmail = ' + str(round(time.time()) - MstrCntrl.prevTime2))
    for ii in range(0,3):
        if gmailMsgCheck():
            break

def gmailMsgCheck():
    Cond_2 = False
    Cond_3 = False
    try:
        MstrCntrl.gmailCntrl.loginIMAP()
        if (MstrCntrl.gmailCntrl.checkExist('MasterUnlock')):
            Cond_2 = MstrCntrl.gmailCntrl.checkFrom([MstrCntrl.AllowList[0]])
            Cond_3 = MstrCntrl.gmailCntrl.checkTime()
            if (Cond_2 and Cond_3):
                MstrCntrl.masterUnlock = True
                MstrCntrl.MasterSTATE = 'UNLOCK'
                MstrCntrl.emailUnlock = True
                MstrCntrl.scheduleSkip = 1
            MstrCntrl.gmailCntrl.clearInfo()

        elif (MstrCntrl.gmailCntrl.checkExist('RelayOff')):
            MstrCntrl.gpioCntrl.RelayOff()
            MstrCntrl.gmailCntrl.clearInfo()

        elif (MstrCntrl.gmailCntrl.checkExist('Lock')):
            MstrCntrl.gpioCntrl.closeLock()
            MstrCntrl.gmailCntrl.clearInfo()

        elif (MstrCntrl.gmailCntrl.checkExist('Status')):
            if (MstrCntrl.gpioCntrl.checkReed()):
                temp = 'Closed'
            else:
                temp = 'Opened'
            MstrCntrl.gmailCntrl.sendTxt(MstrCntrl.AllowList[0][2],
                                         'Current State:' + MstrCntrl.MasterSTATE + '\n Door is: ' + str(temp) + '\nTime: ' +
                                          MstrCntrl.timeNow + '\n Day: ' + str(datetime.datetime.today().weekday()))
            MstrCntrl.gmailCntrl.clearInfo()

        elif (MstrCntrl.gmailCntrl.checkExist('Unlock')):
            if(MstrCntrl.gmailCntrl.checkTime()):
                if MstrCntrl.gmailCntrl.checkFrom(MstrCntrl.AllowList) or MstrCntrl.gmailCntrl.checkFrom(MstrCntrl.AllowListAlt):
                    MstrCntrl.MasterSTATE = 'VERIFY'
                    MstrCntrl.selectedDevice = MstrCntrl.gmailCntrl.Selected
                    MstrCntrl.gmailCntrl.clearInfo()
                    MstrCntrl.emailUnlock = True
                    #if not scheduleCheck():
                    MstrCntrl.scheduleSkip = 1

            else:
                print(' time fail')

        MstrCntrl.gmailCntrl.logoutIMAP()
        return True
    except:
        print('GMail error')
        return False

###############  ISR Definitions ##############
def buttonISR(channel):
    time.sleep(0.01)

    if (MstrCntrl.gpioCntrl.checkOpenButton() and (not MstrCntrl.buttonISR)):
        print("Real button!")
        MstrCntrl.buttonISR = True
        MstrCntrl.scheduleSkip = 1

        if (not MstrCntrl.unlockFreeze):
            MstrCntrl.gpioCntrl.openLock()
            MstrCntrl.MasterSTATE = 'UNLOCK'

            if MstrCntrl.gpioCntrl.checkOpenButton():
                MstrCntrl.gpioCntrl.RelayOn()
                time.sleep(0.1)
                MstrCntrl.gpioCntrl.RelayOff()
                time.sleep(0.1)
                MstrCntrl.gpioCntrl.RelayOn()
                time.sleep(0.1)
                MstrCntrl.gpioCntrl.RelayOff()
                MstrCntrl.unlockFreeze = True

        else:
            print('UnlockFreeze Off')
            MstrCntrl.unlockFreeze = False


def reedISR(channel):
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