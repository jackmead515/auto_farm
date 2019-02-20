import json
import os

def initialize():
    global vals
    vals = defaults()
    load()

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
        "cameras": False,
        "buzzer": False
    }

def defaults():
    return {

        "imagedb": "jack_farm",
        "imagedb_username": "jack",
        "imagedb_password": "",
        "imagedb_host": "",

        "pump_time": 10, # maximum number of seconds pump can be active
        "pump_interval": 30, # min interval at which the pump is then allowed to turn on
        "pump_mode": "auto",

        "image_interval": 30, # min interval at which to take an image
        "morning_time": 5, # time to turn on grow lights in military time hours
        "night_time": 20, # time to turn off grow lights in military time hours
        "day_temp": 26, # temperature to adjust too during the day hours
        "night_temp": 24, # temperature to adjust too during the night hours
        "heat_time": 10, #maxmimum amount of min time the heat lights can be one in case the temperature probes error

        "soil_calibration_values": {},
        "soil_sensor_limit": 60000, # 0-100 analog read of the soil sensors.
        "soil_sensor_channels": [0, 1, 2, 3],
        "water_level_channel": 4,

        "heat_lights_pin": 23,
        "grow_lights_pin": 22,
        "pump_pin": 24,
        "buzzer_pin": 14,

        "grow_lights_enabled": True,
        "pump_enabled": True,
        "heat_lights_enabled": True,
        "cameras_enabled": True,

        "soil_calibrating": False,
        "current_soil": [],
        "current_temp": None,
        "current_humid": None,
        "current_water_level": None

        #"analog_sensor_pins": [10, 9, 25, 11], # When using MCP3008 ADC Converter
        #"tphd_sensor_pins": [15, 18], #, 17, 27],
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
