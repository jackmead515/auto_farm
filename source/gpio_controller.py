'''
sudo apt-get update
sudo apt-get install python-dev python-pip

sudo pip install --upgrade distribute
sudo pip install ipython
sudo pip install --upgrade RPi.GPIO
'''
import RPi.GPIO as GPIO

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

def activate_pin(pin):
    GPIO.output(pin, GPIO.LOW)

def deactivate_pin(pin):
    GPIO.output(pin, GPIO.HIGH)
