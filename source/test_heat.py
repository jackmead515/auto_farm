import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT, initial=GPIO.HIGH)

GPIO.output(23, GPIO.LOW)
time.sleep(30)
GPIO.output(23, GPIO.HIGH)
