import json
import os

def initalize():
    global vals
    vals = defaults()

    global stats
    stats = {
        "pump": False,
        "growlights": False,
        "soilsensors": False,
        "tphdsensors": False,
        "heatlights": False,
        "cameras": False
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

def defaults():
    return {
        "image_dir": "/home/pi/auto_farm/images",
        "max_pump_time": 10, # maximum number of seconds pump can be online
        "soil_interval": 60, # second interval at which to take a soil moisture reading
        "tphd_interval": 60, # second interval at which to take a temperature and humidity reading
        "image_interval": 60*30, # second interval at which to take an image
        "morning_time": 5, # time to turn on grow lights in military time hours
        "night_time": 20, # time to turn off grow lights in military time hours
        "day_temp": 26, # temperature to adjust too during the day hours
        "night_temp": 24, # temperature to adjust too during the night hours
        #"min_day_temp": 24, # minmium temperature in celcius to turn on heat lights during the day
        #"max_day_temp": 28, # maximum temperature in celcius to turn off heat lights during the day
        #"min_night_temp": 24, # minmium temperature in celcius to turn on heat lights during the night
        #"max_night_temp": 27, # maximum temperature in celcius to turn off heat lights during the night
        "soil_sensor_pins": [2, 3, 4, 14],
        "tphd_sensor_pins": [15, 18], #, 17, 27],
        "heat_lights_pin": 23,
        "grow_lights_pin": 22,
        "pump_pin": 24
    }

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
