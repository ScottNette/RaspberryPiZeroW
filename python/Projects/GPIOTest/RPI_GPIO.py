import RPi.GPIO as GPIO
import time

gpioRelay = 3
gpioServoPWM = 18
gpioReed = 4
gpioButton = 17


GPIO.setmode(GPIO.BCM)
GPIO.setup(gpioButton, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(gpioRelay, GPIO.OUT)


GPIO.setup(gpioServoPWM, GPIO.OUT)

pwmServo = GPIO.PWM(gpioServoPWM, 50)
pwmServo.start(2.5)

def my_callback(channel):
    print "falling edge detected on 17"
    GPIO.output(gpioRelay, True)
    print("changed to 2")
    time.sleep(.5)
    pwmServo.ChangeDutyCycle(9)
    time.sleep(1.5)

    GPIO.output(gpioRelay, False)


GPIO.add_event_detect(gpioButton, GPIO.RISING, callback=my_callback, bouncetime=1000)

try:
    print "Waiting for rising edge on port 24"
    while True:


        #GPIO.output(03, True)


        pwmServo.ChangeDutyCycle(4)



        #time.sleep(5)

        pass
    print "Rising edge detected on port 24. Here endeth the third lesson."

except KeyboardInterrupt:
    GPIO.cleanup()  # clean up GPIO on CTRL+C exit
GPIO.cleanup()  # clean up GPIO on normal exit