'''
sudo apt-get update
sudo apt-get install python-dev python-pip

sudo pip install --upgrade distribute
sudo pip install ipython
sudo pip install --upgrade RPi.GPIO
'''
import RPi.GPIO as GPIO
import os
import glob
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

import values

analog_channels = []

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    os.system('sudo modprobe w1-gpio')
    os.system('sudo modprobe w1-therm')

    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
    cs = digitalio.DigitalInOut(board.D25)
    mcp = MCP.MCP3008(spi, cs)
    analog_channels.append(AnalogIn(mcp, MCP.P0))
    analog_channels.append(AnalogIn(mcp, MCP.P1))
    analog_channels.append(AnalogIn(mcp, MCP.P2))
    analog_channels.append(AnalogIn(mcp, MCP.P3))
    analog_channels.append(AnalogIn(mcp, MCP.P4))
    analog_channels.append(AnalogIn(mcp, MCP.P5))
    analog_channels.append(AnalogIn(mcp, MCP.P6))
    analog_channels.append(AnalogIn(mcp, MCP.P7))

def activate_pin(pin):
    GPIO.output(pin, GPIO.LOW)

def deactivate_pin(pin):
    GPIO.output(pin, GPIO.HIGH)

def get_onewiredevices():
    return glob.glob('/sys/bus/w1/devices/28*')

def read_channel(channel):
    c = analog_channels[channel]
    return c.value
