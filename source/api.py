from flask import Flask
from flask import request
from flask import jsonify
from flask import send_from_directory
from flask_cors import CORS

import datetime
import os
import threading

import data
import values
import sensors
import watch

app = Flask(__name__, static_folder='interface')
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def interface(path):
    if path != "" and os.path.exists("interface/" + path):
        return send_from_directory('interface', path)
    else:
        return send_from_directory('interface', 'index.html')

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
        if sensor == "temp":
            if values.status()["tpprobes"] is False:
                reading = sensors.tpprobes.read(values.DEBUG)
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
    elif sensor is not None and sensor != "temp" and sensor != "soil":
        return "Pass a sensor value of 'temp', 'soil'"
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
@app.route('/data/images', methods = ['POST'])
def images():
    params = request.get_json()
    d = data.get_images(params["index"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/data/image', methods = ['POST'])
def image():
    params = request.get_json()
    d = data.get_image(params["name"])
    return jsonify({'data': d})

########################################################################################################################
@app.route('/calibrate/soil', methods = ['POST'])
def calibrate_soil():
    if values.values()["soil_calibrating"] is True:
        return "Sensors are currently calibrating"
    else:
        threading.Thread(target=start_soil_calibration).start()
        return jsonify({'data': 200})

def start_soil_calibration():
    watch.soil_watch.shutdown()
    sensors.soilsensor.calibrate(values.DEBUG)
    watch.soil_watch = watch.SoilWatch()
    watch.soil_watch.start()

########################################################################################################################
@app.route('/submit/pump_control', methods = ['POST'])
def pump_control():
    params = request.get_json()
    validation = validate_pump_control(params)
    if validation is not None:
        return validation
    else:
        values.set_value(["pump_enabled", params["pump_enabled"]])
        values.set_value(["pump_time", params["pump_time"]])
        values.set_value(["pump_interval", params["pump_interval"]])
        values.set_value(["pump_mode", params["pump_mode"]])
        values.set_value(["soil_sensor_limit", params["soil_sensor_limit"]])
        values.save()
        return jsonify({'data': 200})

def validate_pump_control(params):
    if params is None:
        return "Pass the proper parameters argument"
    else:
        if "pump_enabled" in params and "pump_time" in params and "pump_interval" in params and "pump_mode" in params and "soil_sensor_limit" in params:
            return None
        else:
            return "Pass the proper parameters argument"

########################################################################################################################
@app.route('/submit/growlight_control', methods = ['POST'])
def growlight_control():
    params = request.get_json()
    validation = validate_growlight_control(params)
    if validation is not None:
        return validation
    else:
        values.set_value(["grow_lights_enabled", params["grow_lights_enabled"]])
        values.set_value(["morning_time", params["morning_time"]])
        values.set_value(["night_time", params["night_time"]])
        values.save()
        return jsonify({'data': 200})

def validate_growlight_control(params):
    if params is None:
        return "Pass the proper parameters argument"
    else:
        if "grow_lights_enabled" in params and "morning_time" in params and "night_time" in params:
            return None
        else:
            return "Pass the proper parameters argument"

########################################################################################################################
@app.route('/submit/heat_control', methods = ['POST'])
def heat_control():
    params = request.get_json()
    validation = validate_heat_control(params)
    if validation is not None:
        return validation
    else:
        values.set_value(["heat_lights_enabled", params["heat_lights_enabled"]])
        values.set_value(["heat_time", params["heat_time"]])
        values.set_value(["day_temp", params["day_temp"]])
        values.set_value(["night_temp", params["night_temp"]])
        values.save()
        return jsonify({'data': 200})

def validate_heat_control(params):
    if params is None:
        return "Pass the proper parameters argument"
    else:
        if "heat_lights_enabled" in params and "heat_time" in params and "day_temp" in params and "night_temp" in params:
            return None
        else:
            return "Pass the proper parameters argument"

########################################################################################################################
@app.route('/submit/camera_control', methods = ['POST'])
def camera_control():
    params = request.get_json()
    validation = validate_camera_control(params)
    if validation is not None:
        return validation
    else:
        values.set_value(["cameras_enabled", params["cameras_enabled"]])
        values.set_value(["image_interval", params["image_interval"]])
        values.set_value(["imagedb_host", params["imagedb_host"]])
        values.set_value(["imagedb_username", params["imagedb_username"]])
        values.set_value(["imagedb_password", params["imagedb_password"]])
        values.set_value(["imagedb", str(params["imagedb_username"] + "_farm")])
        values.save()
        return jsonify({'data': 200})

def validate_camera_control(params):
    if params is None:
        return "Pass the proper parameters argument"
    else:
        if "cameras_enabled" in params and "image_interval" in params and "imagedb_host" in params and "imagedb_username" in params and "imagedb_password" in params:
            return None
        else:
            return "Pass the proper parameters argument"
