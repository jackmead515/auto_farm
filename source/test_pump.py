import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(24, GPIO.OUT, initial=GPIO.HIGH)

GPIO.output(24, GPIO.LOW)
time.sleep(10)
GPIO.output(24, GPIO.HIGH)
