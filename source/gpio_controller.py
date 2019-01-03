'''
sudo apt-get update
sudo apt-get install python-dev python-pip

sudo pip install --upgrade distribute
sudo pip install ipython
sudo pip install --upgrade RPi.GPIO
'''
import RPi.GPIO as GPIO
import Adafruit_MCP3008

import values

analog_reader = None

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    pins = values.values()["analog_sensor_pins"]
    mcp3008 = Adafruit_MCP3008.MCP3008(clk=pins[0], cs=pins[1], miso=pins[2], mosi=pins[3])

def activate_pin(pin):
    GPIO.output(pin, GPIO.LOW)

def deactivate_pin(pin):
    GPIO.output(pin, GPIO.HIGH)

def read_channel(channel):
    return analog_reader.read_adc(channel)
