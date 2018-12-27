#from multiprocessing import Pool
import threading
import time
import os

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
        pass

    def deact(self, log = False):
        if log:
            print("Powering water pump off")
        gpio.power_off_pump()
        values.set_status(["pump", False])

    def act(self, log = False):
        values.set_status(["pump", True])
        if log:
            print("Powering water pump on")
        gpio.power_on_pump()
        time.sleep(values.values()["max_pump_time"])
        if log:
            print("Powering water pump off")
        gpio.power_off_pump()
        values.set_status(["pump", False])


################################################################################################################
class GrowLights(Sensor):

    def __init__(self):
        pass

    def deact(self, log = False):
        if log:
            print("Powering grow lights off")
        gpio.power_off_grow_lights()
        values.set_status(["growlights", False])

    def act(self, log = False):
        values.set_status(["growlights", True])
        if log:
            print("Powering grow lights on")
        gpio.power_on_grow_lights()



################################################################################################################
class HeatLights(Sensor):

    def __init__(self):
        pass

    def deact(self, log = False):
        if log:
            print("Powering heat lamps off")
        gpio.power_off_heat_lights()
        values.set_status(["heatlights", False])

    def act(self, log = False):
        values.set_status(["heatlights", True])
        if log:
            print("Powering heat lamps on")
        gpio.power_on_heat_lights()


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
        pass

    def read(self, log = False):
        if log:
            print("Reading soil sensors")
        values.set_status(["soilsensors", True])
        readings = gpio.read_soil_sensors()
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
        readings = gpio.read_tphd_sensors()
        values.set_status(["tphdsensors", False])
        return readings
