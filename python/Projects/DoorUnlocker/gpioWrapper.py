from gpiozero import Servo
import wiringpi
import time


wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pinMode(23, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pinMode(17, wiringpi.GPIO.INPUT)
wiringpi.pinMode(24, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(17,wiringpi.PUD_DOWN)
wiringpi.pullUpDnControl(23,wiringpi.PUD_DOWN)
wiringpi.pullUpDnControl(24,wiringpi.PUD_DOWN)


# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)



class gpioWrapper:
    def __init__(self):
        # use 'GPIO naming'


        self.delay_period = 0.01
        self.openDoor = 0
        self.closeDoor = 1

        self.gpioRelay = 23
        self.gpioServoPWM = 18
        self.gpioServoFB = 25
        self.gpioReed  = 17
        self.gpioButton = 24

    def checkReed(self):
        sampleVal = []
        for ii in range(0,3,1):
            sampleVal.append(wiringpi.digitalRead(self.gpioReed))
            time.sleep(0.1)
        return len(set(sampleVal)) <= 1

    def checkOpenButton(self):
        return wiringpi.digitalRead(self.gpioButton)

    def openLock(self):
        wiringpi.digitalWrite(self.gpioRelay, 1)
        for pulse in range(50, 250, 1):
            wiringpi.pwmWrite(self.gpioServoPWM, pulse)
            time.sleep(self.delay_period)
        wiringpi.digitalWrite(self.gpioRelay, 0)

    def closeLock(self):
        wiringpi.digitalWrite(self.gpioRelay, 1)
        for pulse in range(250, 50, -1):
            wiringpi.pwmWrite(self.gpioServoPWM, pulse)
            time.sleep(self.delay_period)
        wiringpi.digitalWrite(self.gpioRelay, 0)

