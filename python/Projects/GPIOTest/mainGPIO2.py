import time
import wiringpi

# use 'GPIO naming'
wiringpi.wiringPiSetupGpio()

# set #18 to be a PWM output
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pinMode(17, wiringpi.GPIO.INPUT)
wiringpi.pullUpDnControl(17,wiringpi.PUD_DOWN)

# set the PWM mode to milliseconds stype
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

wiringpi.pinMode(3, wiringpi.GPIO.OUTPUT)

# divide down clock
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period = 0.01

wiringpi.digitalWrite(3, 00.5
                      )

while True:


    for pulse in range(50, 250, 1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
    time.sleep(2)
    for pulse in range(250, 50, -1):
        wiringpi.pwmWrite(18, pulse)
        time.sleep(delay_period)
    time.sleep(2)

    print(wiringpi.digitalRead(17))
    time.sleep(0.2)
