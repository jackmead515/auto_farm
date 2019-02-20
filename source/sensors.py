#from multiprocessing import Pool
import threading
import time
import statistics as stats
import os

import RPi.GPIO as GPIO
import Adafruit_DHT
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import gpio_controller as gpio
import usb_controller as usb
import data
import values

def initialize():
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
    display = OLEDDisplay()

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
            usb.snap_photo(camera, '/home/pi/auto_farm/images', name)

        if log:
            print("Attempting to upload images")
        total = 0
        files = os.listdir('/home/pi/auto_farm/images')
        for f in files:
            path = os.path.join('/home/pi/auto_farm/images', f)
            if total >= 16:
                break
            if os.path.isfile(path) and f.endswith('.png'):
                try:
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

    def calibrate(self, log = False):
        if log:
            print("Calibrating soil sensors")
        values.set_status(["soil_calibrating", True])

        data = {}
        for i in range(120): # 2 minutes
            for channel in values.values()["soil_sensor_channels"]:
                if str(channel) not in data:
                    data[str(channel)] = []
                value = gpio.read_channel(channel)
                if value >= 20000:
                    data[str(channel)].append({"v": value, "p": channel})
            time.sleep(1)
        calvals = {}
        for key in data:
            vs = []
            for kp in data[key]:
                vs.append(kp["v"])
            median = stats.median(vs)
            stdev = stats.stdev(vs)
            calvals[key] = {'median': median, 'std': stdev}

        values.set_value(["soil_calibration_values", calvals])
        values.set_status(["soil_calibrating", False])
        if log:
            print("Calibrating soil sensors completed")

    def read(self, log = False):
        if log:
            print("Reading soil sensors")
        values.set_status(["soilsensors", True])

        readings = []
        for channel in values.values()["soil_sensor_channels"]:
            value = gpio.read_channel(channel)
            if value >= 20000:
                readings.append({"value": value, "pin": channel})

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
class OLEDDisplay:

    def __init__(self):
        self.display = None
        self.draw = None
        self.width = None
        self.height = None
        self.font = None

    def initialize(self):
        self.display = Adafruit_SSD1306.SSD1306_128_64(rst=0)
        self.display.begin()
        self.display.clear()
        self.display.display()
        self.width = self.display.width
        self.height = self.display.height
        self.image = Image.new('1', (self.width, self.height))
        self.draw = ImageDraw.Draw(self.image)
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)

    def refresh(self):
        self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)
        self.display.clear()
        self.display.display()

        humid = 0.0
        temp = 0.0
        if values.values()["current_temp"] is not None:
            temp = round(float(values.values()["current_temp"]), 1)
        if values.values()["current_humid"] is not None:
            humid = round(float(values.values()["current_humid"]), 1)

        self.draw.text((0, 5), "T " + str(temp) + u"\u00b0C", font=self.font, fill=255)
        self.draw.text((0, 35), "H " + str(humid) + "%",  font=self.font, fill=255)
        self.display.image(self.image)
        self.display.display()
################################################################################################################
