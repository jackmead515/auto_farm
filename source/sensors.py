#from multiprocessing import Pool
import threading
import time
import os

import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_MCP3008

import gpio_controller as gpio
import usb_controller as usb
import values

def initalize():
    global pump, growlights, heatlights, soilsensor, thsensor, cameras

    pump = Pump()
    growlights = GrowLights()
    heatlights = HeatLights()
    soilsensor = SoilSensors()
    thsensor = TPHDSensors()
    cameras = Cameras()

################################################################################################################
class Sensor:

    def __init__(self):
        pass

    def deactivate(self, log = False):
        threading.Thread(target=self.deact, args=(log,)).start()

    def activate(self, log = False):
        threading.Thread(target=self.act, args=(log,)).start()

    def deact(self, log = False):
        pass

    def act(self, log = False):
        pass

################################################################################################################
class Pump(Sensor):

    def __init__(self):
        GPIO.setup(values.values()["pump_pin"], GPIO.OUT, initial=GPIO.HIGH)

    def deact(self, log = False):
        if log:
            print("Powering water pump off")
        gpio.power_off_pump()
        values.set_status(["pump", False])

    def act(self, log = False):
        values.set_status(["pump", True])
        if log:
            print("Powering water pump on")
        gpio.activate_pin(values.values()["pump_pin"])
        time.sleep(values.values()["max_pump_time"])
        if log:
            print("Powering water pump off")
        gpio.deactivate_pin(values.values()["pump_pin"])
        values.set_status(["pump", False])


################################################################################################################
class GrowLights(Sensor):

    def __init__(self):
        GPIO.setup(values.values()["grow_lights_pin"], GPIO.OUT, initial=GPIO.HIGH)

    def deact(self, log = False):
        if log:
            print("Powering grow lights off")
        gpio.deactivate_pin(values.values()["grow_lights_pin"])
        values.set_status(["growlights", False])

    def act(self, log = False):
        values.set_status(["growlights", True])
        if log:
            print("Powering grow lights on")
        gpio.activate_pin(values.values()["grow_lights_pin"])



################################################################################################################
class HeatLights(Sensor):

    def __init__(self):
        GPIO.setup(values.values()["heat_lights_pin"], GPIO.OUT, initial=GPIO.HIGH)

    def deact(self, log = False):
        if log:
            print("Powering heat lamps off")
        gpio.deactivate_pin(values.values()["heat_lights_pin"])
        values.set_status(["heatlights", False])

    def act(self, log = False):
        values.set_status(["heatlights", True])
        if log:
            print("Powering heat lamps on")
        gpio.activate_pin(values.values()["heat_lights_pin"])


################################################################################################################
class Cameras(Sensor):

    def __init__(self):
        pass

    def act(self, log = False):
        values.set_status(["cameras", True])
        if log:
            print("Taking images")
        cameras = usb.get_usb_cameras()
        for camera in cameras:
            name = os.path.basename(camera) + '_' + str(round(time.time())) + '.jpg'
            image = usb.snap_photo(camera, values.values()["image_dir"], name)

        values.set_status(["cameras", False])


################################################################################################################
class SoilSensors:

    def __init__(self):
        if values.values()["soil_sensor_type"] == 'digital':
            for pin in values.values()["digital_soil_sensor_pins"]:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        elif values.values()["soil_sensor_type"] == 'analog':
            pins = values.values()["analog_sensor_pins"]
            self.reader = Adafruit_MCP3008.MCP3008(clk=pins[0], cs=pins[1], miso=pins[2], mosi=pins[3])

    def read(self, log = False):
        if log:
            print("Reading soil sensors")
        values.set_status(["soilsensors", True])

        readings = []
        if values.values()["soil_sensor_type"] == 'digital':

            for pin in values.values()["digital_soil_sensor_pins"]:
                readings.append({"value": GPIO.input(pin), "pin": pin})

        elif values.values()["soil_sensor_type"] == 'analog':

            for channel in values.values()["soil_sensor_channels"]:
                value = self.reader.read_adc(channel)
                readings.append({"value": value, "pin": channel})

        values.set_status(["soilsensors", False])
        return readings


################################################################################################################
class TPHDSensors:

    def __init__(self):
        pass

    def read(self, log = False):
        if log:
            print("Reading temperature/humidity sensors")
        values.set_status(["tphdsensors", True])

        readings = []
        for pin in values.values()["tphd_sensor_pins"]:
            humid, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
            readings.append({"humid": humid, "temp": temp, "pin": pin})

        values.set_status(["tphdsensors", False])
        return readings








###
