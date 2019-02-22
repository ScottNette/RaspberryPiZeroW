import RPi.GPIO as GPIO
import subprocess
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(3, GPIO.OUT)
GPIO.output(3, 0)

try:
    proc = subprocess.call('python /home/pi/Projects/DoorUnlocker/mainDoorUnlocker.py', shell=True)
    #while True:
    #    pass

except KeyboardInterrupt:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, 0)
    os.system("killall python")
    subprocess.call(['killall python'])
    subprocess.call(['pkill -9 python'])
    proc.terminate()


finally:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(3, GPIO.OUT)
    GPIO.output(3, 0)
    os.system("killall python")
    subprocess.call(['killall python'])
    subprocess.call(['pkill -9 python'])
    proc.terminate()