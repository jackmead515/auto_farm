'''
sudo apt-get update
sudo apt-get install python-dev python-pip

sudo pip install --upgrade distribute
sudo pip install ipython
sudo pip install --upgrade RPi.GPIO
'''
import values
import RPi.GPIO as GPIO
import Adafruit_DHT

def initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    for pin in values.values()["soil_sensor_pins"]:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(values.values()["heat_lights_pin"], GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(values.values()["grow_lights_pin"], GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(values.values()["pump_pin"], GPIO.OUT, initial=GPIO.HIGH)

def read_soil_sensors():
    readings = []
    for pin in values.values()["soil_sensor_pins"]:
        readings.append({"value": GPIO.input(pin), "pin": pin})
    return readings

def read_tphd_sensors():
    readings = []
    for pin in values.values()["tphd_sensor_pins"]:
        humid, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        readings.append({"humid": humid, "temp": temp, "pin": pin})
    return readings

def power_on_heat_lights():
    GPIO.output(values.values()["heat_lights_pin"], GPIO.LOW)

def power_off_heat_lights():
    GPIO.output(values.values()["heat_lights_pin"], GPIO.HIGH)

def power_on_grow_lights():
    GPIO.output(values.values()["grow_lights_pin"], GPIO.LOW)

def power_off_grow_lights():
    GPIO.output(values.values()["grow_lights_pin"], GPIO.HIGH)

def power_on_pump():
    GPIO.output(values.values()["pump_pin"], GPIO.LOW)

def power_off_pump():
    GPIO.output(values.values()["pump_pin"], GPIO.HIGH)
