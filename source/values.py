import json
import os

def initalize():
    global vals
    vals = defaults()

    global DEBUG
    DEBUG = True

    global stats
    stats = {
        "pump": False,
        "growlights": False,
        "soilsensors": False,
        "tpprobes": False,
        "heatlights": False,
        "wlsensor": False,
        "cameras": False
    }

def defaults():
    return {
        "image_dir": "/home/pi/auto_farm/images",
        "imagedb_host": "192.168.1.16",
        "max_pump_time": 10, # maximum number of seconds pump can be active
        "pump_interval": 60*30, # second interval at which the pump is then allowed to turn on
        "soil_interval": 30, # second interval at which to take a soil moisture reading
        "tp_interval": 10, # second interval at which to take a temperature and humidity reading
        "image_interval": 60*30, # second interval at which to take an image
        "morning_time": 5, # time to turn on grow lights in military time hours
        "night_time": 20, # time to turn off grow lights in military time hours
        "day_temp": 26, # temperature to adjust too during the day hours
        "night_temp": 24, # temperature to adjust too during the night hours
        "soil_sensor_limit": 60, # 0-100 analog read of the soil sensors.
        "soil_sensor_channels": [0, 1, 2, 3],
        #"analog_sensor_pins": [10, 9, 25, 11], # When using MCP3008 ADC Converter
        #"tphd_sensor_pins": [15, 18], #, 17, 27],
        "heat_lights_pin": 23,
        "grow_lights_pin": 22,
        "pump_pin": 24,
        "wlsensor_channel": 4,

        "current_temp": 0.0,
        "current_soil": [],
        "current_humid": 0.0
    }

def values():
    return vals

def status():
    return stats

def set_value(l):
    if l[0] in vals:
        vals[l[0]] = l[1]

def set_status(l):
    if l[0] in stats:
        stats[l[0]] = l[1]

def load():
    if os.path.isfile('./values.json'):
        with open('./values.json', 'r') as f:
            v = json.load(f)
            vals = v
    else:
        with open('./values.json', 'w') as f:
            json.dump(defaults(), f)
            vals = defaults()

def save():
    with open('./values.json', 'w') as f:
        json.dump(vals, f)
