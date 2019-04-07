from gpiozero import Servo
import RPi.GPIO as GPIO
import time




class gpioWrapper:
    def __init__(self):
        # use 'GPIO naming'


        self.delay_period = 0.01
        self.openDoor = False
        self.closeDoor = True

        self.pwmLockCmd = 9.5
        self.pwmUnlockCmd = 4

        self.gpioRelay = 3
        self.gpioServoPWM = 18
        self.gpioReed  = 4
        self.gpioButton = 17
        self.gpioLED = 16

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioReed, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.gpioButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.gpioRelay, GPIO.OUT)
        GPIO.setup(self.gpioServoPWM, GPIO.OUT)
        GPIO.setup(self.gpioLED, GPIO.OUT)

        self.pwmServo = GPIO.PWM(self.gpioServoPWM, 50)
        self.pwmServo.start(0)

    def relayGPIOSetup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioRelay, GPIO.OUT)


    def checkReed(self):
        sampleVal = []
        for ii in range(0,15,1):
            sampleVal.append(GPIO.input(self.gpioReed))
            time.sleep(0.05)
        #return len(set(sampleVal)) <= 1
        if sum(sampleVal) > 13 :  # :)
            return True
        else:
            return False


    def checkOpenButton(self):
        sampleVal = []
        for ii in range(0, 15, 1):
            sampleVal.append(GPIO.input(self.gpioButton))
            time.sleep(0.01)
        if sum(sampleVal) > 13:
            return True
        else:
            return False


    def openLock(self):
        self.RelayOn()
        time.sleep(0.1)
        self.pwmServo.ChangeDutyCycle(self.pwmLockCmd)
        time.sleep(2)
        self.ServoOff()
        self.RelayOff()


    def closeLock(self):
        self.RelayOn()
        time.sleep(0.1)
        self.pwmServo.ChangeDutyCycle(self.pwmUnlockCmd)
        time.sleep(3)
        self.ServoOff()
        self.RelayOff()


    def ServoOff(self):
        self.pwmServo.ChangeDutyCycle(0)

    def RelayOff(self):
        GPIO.output(self.gpioRelay, 0)

    def RelayOn(self):
        GPIO.output(self.gpioRelay, 1)

    def LEDOff(self):
        GPIO.output(self.gpioLED, 0)

    def LEDOn(self):
        GPIO.output(self.gpioLED, 1)