from gpiozero import Servo
import RPi.GPIO as GPIO
import time




class gpioWrapper:
    def __init__(self):
        # use 'GPIO naming'


        self.delay_period = 0.01
        self.openDoor = 0
        self.closeDoor = 1

        self.pwmLockCmd = 9
        self.pwmUnlockCmd = 4

        self.gpioRelay = 3
        self.gpioServoPWM = 18
        self.gpioReed  = 17
        self.gpioButton = 4

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioReed, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.gpioButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.gpioRelay, GPIO.OUT)
        GPIO.setup(self.gpioServoPWM, GPIO.OUT)

        self.pwmServo = GPIO.PWM(self.gpioServoPWM, 50)
        self.pwmServo.start(0)



    def checkReed(self):
        sampleVal = []
        for ii in range(0,15,1):
            sampleVal.append(GPIO.input(self.gpioReed))
            time.sleep(0.1)
        #return len(set(sampleVal)) <= 1
        if sampleVal == [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]:  # :)
            return True
        else:
            return False


    def checkOpenButton(self):
        sampleVal = []
        for ii in range(0, 15, 1):
            sampleVal.append(GPIO.input(self.gpioButton))
            time.sleep(0.01)
        # return len(set(sampleVal)) <= 1
        if sampleVal == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:  # :)
            return True
        else:
            return False



    def openLock(self):
        GPIO.output(self.gpioRelay, 1)

        time.sleep(0.5)
        self.pwmServo.ChangeDutyCycle(self.pwmLockCmd)
        time.sleep(1.5)
        self.pwmServo.ChangeDutyCycle(0)

        GPIO.output(self.gpioRelay, 0)
        #self.pwmServo.stop()

    def closeLock(self):
        GPIO.output(self.gpioRelay, 1)

        time.sleep(0.5)
        self.pwmServo.ChangeDutyCycle(self.pwmUnlockCmd)
        time.sleep(1.5)
        self.pwmServo.ChangeDutyCycle(0)

        GPIO.output(self.gpioRelay, 0)
        #self.pwmServo.stop()
