from gpiozero import Servo
import wiringpi
import time


wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pinMode(17, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(17,wiringpi.PUD_DOWN)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)



class gpioWrapper:
    def __init__(self):
        # use 'GPIO naming'


        self.delay_period = 0.01

    def checkReed(self):
        return wiringpi.digitalRead(17)

    def checkOpenButton(self):
        return wiringpi.digitalRead(15)

    def openLock(self):
        for pulse in range(50, 250, 1):
            wiringpi.pwmWrite(18, pulse)
            time.sleep(self.delay_period)

    def closeLock(self):
        for pulse in range(250, 50, -1):
            wiringpi.pwmWrite(18, pulse)
            time.sleep(self.delay_period)

