from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory
from flask_cors import CORS

import os

import data
import values
import sensors

app = Flask(__name__, static_url_path='/home/pi/auto_farm/')
CORS(app)

########################################################################################################################
@app.route('/activate/<sensor>/<value>', methods = ['POST'])
def activate(sensor, value):
    validation = validate_activate(sensor, value)
    if validation is not None:
        return validation
    else:
        if sensor == "pump":

            if int(value) == 1:
                if values.status()["pump"] is False:
                    sensors.pump.activate(values.DEBUG)
                    return "Pump activated"
                else:
                    return "Pump in use"
            elif int(value) == 0:
                sensors.pump.deactivate(values.DEBUG)
                return "Pump deactivated"

        elif sensor == "heatlights":

            if int(value) == 1:
                if values.status()["heatlights"] is False:
                    sensors.heatlights.activate(values.DEBUG)
                    return "Heat lights activated"
                else:
                    return "Heat lights already activated"
            elif int(value) == 0:
                sensors.heatlights.deactivate(values.DEBUG)
                return "Heat lights deactivated"

        elif sensor == "growlights":

            if int(value) == 1:
                if values.status()["growlights"] is False:
                    sensors.growlights.activate(values.DEBUG)
                    return "Grow lights activated"
                else:
                    return "Grow lights already activated"
            elif int(value) == 0:
                sensors.growlights.deactivate(values.DEBUG)
                return "Grow lights deactivated"

        elif sensor == "cameras":

            if values.status()["cameras"] is False:
                sensors.cameras.activate(values.DEBUG)
                return "Cameras taking images"
            else:
                return "Cameras are currently taking images"

def validate_activate(sensor, value):
    if sensor is None or value is None:
        return "Pass a sensor and value argument"
    elif sensor is not None and sensor != "pump" and sensor != "heatlights" and sensor != "growlights" and sensor != "cameras":
        return "Pass a sensor value of 'pump', 'heatlights', 'cameras', or 'growlights'"
    elif value is None or (value is not None and value.isdigit() == False) or (value.isdigit() == True and int(value) != 0 and int(value) != 1):
        return "Pass a value value of 0 or 1"
    else:
        return None

########################################################################################################################
@app.route('/read/<sensor>', methods = ['POST'])
def read(sensor):
    validation = validate_read(sensor)
    if validation is not None:
        return validation
    else:
        if sensor == "temphumid":
            if values.status()["tphdsensors"] is False:
                reading = sensors.thsensor.read(values.DEBUG)
                return jsonify({ 'data': reading })
            else:
                return "Reading is already being taken"
        elif sensor == "soil":
            if values.status()["soilsensors"] is False:
                reading = sensors.soilsensor.read(values.DEBUG)
                return jsonify({ 'data': reading })
            else:
                return "Reading is already being taken"

def validate_read(sensor):
    if sensor is None:
        return "Pass a sensor argument"
    elif sensor is not None and sensor != "temphumid" and sensor != "soil":
        return "Pass a sensor value of 'temphumid', 'soil'"
    else:
        return None

########################################################################################################################
@app.route('/status', methods = ['POST'])
def status():
    d = values.status()
    return jsonify({ 'data': d })

########################################################################################################################
@app.route('/info', methods = ['POST'])
def info():
    d = values.values()
    return jsonify({ 'data': d })

########################################################################################################################
@app.route('/data/temperature', methods = ['POST'])
def temp():
    params = request.get_json()
    d = data.get_temp(params["start"], params["end"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/data/humidity', methods = ['POST'])
def humid():
    params = request.get_json()
    d = data.get_humid(params["start"], params["end"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/data/soil', methods = ['POST'])
def soil():
    params = request.get_json()
    d = data.get_soil(params["start"], params["end"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/data/messages', methods = ['POST'])
def messages():
    d = data.get_messages()
    return jsonify({'data': d})

########################################################################################################################
@app.route('/data/heat', methods = ['POST'])
def heat():
    params = request.get_json()
    d = data.get_heat(params["start"], params["end"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/data/lights', methods = ['POST'])
def lights():
    params = request.get_json()
    d = data.get_lights(params["start"], params["end"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/data/pump', methods = ['POST'])
def pump():
    params = request.get_json()
    d = data.get_pump(params["start"], params["end"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/set/<ttype>/<value>', methods = ['POST'])
def sett(ttype, value):
    validation = validate_set(ttype, value)
    if validation is not None:
        return validation
    else:
        values.set_value([ttype, value])
        return ttype + " value set"

def validate_set(ttype, value):
    if ttype is None or value is None:
        return "Pass a type and value argument"
    elif ttype is not None and ttype not in values.defaults():
        return "Invalid type argument"
    else:
        return None
