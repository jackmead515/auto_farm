#from multiprocessing import Pool
import threading
import time
import os

import RPi.GPIO as GPIO
import Adafruit_DHT
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_SSD1306
#from PIL import Image
#from PIL import ImageDraw
#from PIL import ImageFont

import gpio_controller as gpio
import usb_controller as usb
import data
import values

def initalize():
    global buzzer, display, pump, growlights, heatlights, soilsensor, cameras, wlsensor, tpprobes#, thsensor

    pump = Pump()
    growlights = GrowLights()
    heatlights = HeatLights()
    soilsensor = SoilSensors()
    #thsensor = TPHDSensors()
    tpprobes = TPProbes()
    wlsensor = WLSensor()
    cameras = Cameras()
    buzzer = Buzzer()
    #display = OLEDDisplay()

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
        time.sleep(values.values()["pump_time"])
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
            name = os.path.basename(camera) + '_' + str(round(time.time())) + '.png'
            usb.snap_photo(camera, values.values()["image_dir"], name)

        if log:
            print("Attempting to upload images")
        total = 0
        files = os.listdir(values.values()["image_dir"])
        for f in files:
            if total >= 16:
                break
            if os.path.isfile(f) and f.endswith('.png'):
                try:
                    path = os.path.join(values.values["image_dir"], f)
                    image_data = open(path, 'rb').read()
                    data.save_image(f, image_data)
                    os.remove(path)
                    total+=1
                except Exception as e:
                    if values.DEBUG:
                        print(e)


        values.set_status(["cameras", False])

################################################################################################################
class SoilSensors:

    def __init__(self):
        pass

    def normalize_reading(self, value):
        '''
        Returns a value from 0 to 100. 100 being very wet,
        and 0 being no water present. Value passed should be between
        1.5 and 3.3 correlating to the voltage of the sensor. If the value
        rounded is 0 or is less than 1, returns -1.
        '''
        if value < 1 or round(value) < 1:
            return -1
        else:
            normalized = int((-50 *value)+165)
            if normalized < 0:
                normalized = 0
            if normalized > 100:
                normalized = 100
            return normalized

    def read(self, log = False):
        if log:
            print("Reading soil sensors")
        values.set_status(["soilsensors", True])

        readings = []
        for channel in values.values()["soil_sensor_channels"]:
            value = gpio.read_channel(channel)
            if value >= 0:
                readings.append({"value": self.normalize_reading(value), "pin": channel})

        values.set_status(["soilsensors", False])
        return readings

################################################################################################################
### DHT11
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

################################################################################################################
### DS18B20
class TPProbes:

    def __init__(self):
        pass

    def read_device_file(self, dfile):
        f = open(dfile, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temperature(self, dfile):
        lines = self.read_device_file(dfile)
        start = time.time()
        while lines[0].strip()[-3:] != 'YES':
            if time.time()-start >= 10:
                return -1
            else:
                time.sleep(0.2)
                lines = self.read_device_file(dfile)
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c
        else:
            return -1

    def read(self, log = False):
        if log:
            print("Reading temperature probes")
        values.set_status(["tpprobes", True])

        readings = []
        devices = gpio.get_onewiredevices()
        for device in devices:
            dfile = device + '/w1_slave'
            ctemp = self.read_temperature(dfile)
            readings.append({"temp": ctemp, "pin": 2})

        values.set_status(["tpprobes", False])
        return readings

################################################################################################################
class WLSensor:

    def __init__(self):
        pass

    def read(self, log = False):
        if log:
            print("Reading water level sensors")
        values.set_status(["wlsensor", True])

        readings = []
        channel = values.values()["water_level_channel"]
        value = gpio.read_channel(channel)
        if value >= 0:
            readings.append({"value": value, "pin": channel})

        values.set_status(["wlsensor", False])
        return readings

################################################################################################################
class Buzzer:
    def __init__(self):
        GPIO.setup(values.values()["buzzer_pin"], GPIO.IN)
        GPIO.setup(values.values()["buzzer_pin"], GPIO.OUT)
        self.tones = {
            "start": {
                "pitches": [523,988,1047],
                "duration": [0.2,0.2,0.2]
            },
            "error": {
                "pitches": [262,330,0,262,330,0],
                "duration": [0.5,1,0.5,0.5,1,0.5]
            }
        }

    def activate(self, name, count, log = False):
        threading.Thread(target=self.play, args=(name, count, log,)).start()

    def play(self, name, count, log):
        values.set_status(["buzzer", True])
        for i in range(count):
            x=0
            for p in self.tones[name]["pitches"]:
              buzzer.buzz(p, self.tones[name]["duration"][x])
              time.sleep(self.tones[name]["duration"][x]*0.5)
              x+=1
        values.set_status(["buzzer", False])

    def buzz(self,pitch,duration):
        if(pitch==0):
         time.sleep(duration)
         return
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)

        for i in range(cycles):
         GPIO.output(values.values()["buzzer_pin"], True)
         time.sleep(delay)
         GPIO.output(values.values()["buzzer_pin"], False)
         time.sleep(delay)

################################################################################################################
'''
class OLEDDisplay:

    def __init__(self):
        self.display = None
        self.draw = None
        self.width = None
        self.height = None
        self.font = None

    def initialize():
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=0)
        self.display.begin()
        self.display.clear()
        self.display.display()
        self.width = self.display.width
        self.height = self.display.height
        self.draw = ImageDraw.Draw(Image.new('1', (width, height)))
        self.draw.rectangle((0,0,width,height), outline=0, fill=0)
        self.font = ImageFont.load_default()

    def refresh():
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.display.clear()
        self.display.display()
        self.draw.text((0, 8), "Temperature: " + str(values.values()["current_temp"]), font=self.font, fill=255)
        self.draw.text((0, 16), "Humidity: " + str(values.values()["current_humid"]),  font=self.font, fill=255)
'''
################################################################################################################
