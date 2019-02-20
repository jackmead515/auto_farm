import threading
import time
import datetime
import statistics
import traceback

import values
import data
import util
import sensors

def initialize():
    global pump_watch, heat_watch, light_watch, soil_watch, temp_watch, water_watch, camera_watch

    pump_watch = PumpWatch()
    heat_watch = HeatWatch()
    light_watch = LightWatch()
    soil_watch = SoilWatch()
    temp_watch = TempWatch()
    water_watch = WaterWatch()
    camera_watch = CameraWatch()

def start():
    pump_watch.start()
    heat_watch.start()
    light_watch.start()
    soil_watch.start()
    temp_watch.start()
    water_watch.start()
    camera_watch.start()

def shutdown():
    heat_watch.shutdown()
    light_watch.shutdown()
    pump_watch.shutdown()
    soil_watch.shutdown()
    temp_watch.shutdown()
    water_watch.shutdown()
    camera_watch.shutdown()

########################################################################################################################
########################################################################################################################
########################################################################################################################

class Watch(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.loop = True
    def shutdown(self):
        self.loop = False
        if self.is_alive():
            self.join()
    def on_end(self):
        pass

########################################################################################################################
########################################################################################################################
########################################################################################################################

class PumpWatch(Watch):

    def __init__(self):
        Watch.__init__(self)

    def run(self):
        last_pump_time = time.time()
        while(self.loop):
            try:
                reservoir_has_water = water_watch.reservoir_has_water()
                is_calibrating = values.values()["soil_calibrating"]
                can_pump_again = time.time()-last_pump_time >= values.values()["pump_interval"]*60

                if values.values()["pump_enabled"] is True and reservoir_has_water is True:
                    if values.values()["pump_mode"] is "auto" and can_pump_again is True and is_calibrating is False and soil_watch.soil_needs_water():
                        last_pump_time = time.time()
                        data.save_pump(values.values()["pump_time"])
                        sensors.pump.activate(values.DEBUG)

                    elif values.values()["pump_mode"] is "manual" and can_pump_again is True:
                        last_pump_time = time.time()
                        data.save_pump(values.values()["pump_time"])
                        sensors.pump.activate(values.DEBUG)
                time.sleep(1)
            except Exception:
                if values.DEBUG:
                    traceback.print_exc()

        self.on_end()

########################################################################################################################
########################################################################################################################
########################################################################################################################

class HeatWatch(Watch):
    def __init__(self):
        Watch.__init__(self)

    def on_end(self):
        sensors.heatlights.deactivate(values.DEBUG)

    def run(self):
        disabled = False
        start_disabled_time = 0;
        start_heat_on = 0
        while(self.loop):
            try:
                if values.values()["heat_lights_enabled"] is True and not disabled:
                    if values.status()["heatlights"] is True and time.time()-start_heat_on > values.values()["heat_time"]*60:
                        disabled = True
                        start_disabled_time = time.time()
                        data.save_heat(0)
                        sensors.heatlights.deactivate(values.DEBUG)
                    elif values.status()["heatlights"] is True and values.values()["current_temp"] is None:
                        data.save_heat(0)
                        sensors.heatlights.deactivate(values.DEBUG)
                    elif values.values()["current_temp"] is not None:
                        mt = values.values()["morning_time"]
                        nt = values.values()["night_time"]
                        now = datetime.datetime.now()
                        day_times, night_times = util.time_ranges(mt, nt)
                        if day_times is not None and night_times is not None:
                            if now.hour in day_times:
                                if values.values()["current_temp"] >= values.values()["day_temp"] and values.status()["heatlights"] is True:
                                    data.save_heat(0)
                                    sensors.heatlights.deactivate(values.DEBUG)
                                elif values.values()["current_temp"] < values.values()["day_temp"] and values.status()["heatlights"] is False:
                                    data.save_heat(1)
                                    start_heat_on = time.time()
                                    sensors.heatlights.activate(values.DEBUG)
                            elif now.hour in night_times:
                                if values.values()["current_temp"] >= values.values()["night_temp"] and values.status()["heatlights"] is True:
                                    data.save_heat(0)
                                    sensors.heatlights.deactivate(values.DEBUG)
                                elif values.values()["current_temp"] < values.values()["night_temp"] and values.status()["heatlights"] is False:
                                    data.save_heat(1)
                                    start_heat_on = time.time()
                                    sensors.heatlights.activate(values.DEBUG)
                elif values.status()["heatlights"] is True:
                    data.save_heat(0)
                    sensors.heatlights.deactivate(values.DEBUG)

                if disabled is True and time.time()-start_disabled_time > 300:
                    disabled = False

                time.sleep(1)
            except Exception:
                if values.DEBUG:
                    traceback.print_exc()

        self.on_end()

########################################################################################################################
########################################################################################################################
########################################################################################################################

class LightWatch(Watch):
    def __init__(self):
        Watch.__init__(self)

    def on_end(self):
        sensors.heatlights.deactivate(values.DEBUG)

    def run(self):
        while(self.loop):
            try:
                if values.values()["grow_lights_enabled"] is True:
                    mt = values.values()["morning_time"]
                    nt = values.values()["night_time"]
                    now = datetime.datetime.now()

                    day_times, night_times = util.time_ranges(mt, nt)

                    if day_times is not None and night_times is not None:
                        if now.hour in day_times and values.status()["growlights"] is False:
                            data.save_lights(1)
                            sensors.growlights.activate(values.DEBUG)
                        elif now.hour in night_times and values.status()["growlights"] is True:
                            data.save_lights(0)
                            sensors.growlights.deactivate(values.DEBUG)
                elif values.status()["growlights"] is True:
                    sensors.growlights.deactivate(values.DEBUG)

                time.sleep(1)
            except Exception:
                if values.DEBUG:
                    traceback.print_exc()

        self.on_end()

########################################################################################################################
########################################################################################################################
########################################################################################################################

class SoilWatch(Watch):
    def __init__(self):
        Watch.__init__(self)
        self.soil_stack = {}

    def on_end(self):
        pass

    def soil_needs_water(self):
        soilchannels = values.values()["soil_sensor_channels"]
        calvals = values.values()["soil_calibration_values"]
        total_above_threshold = 0

        if len(soilchannels) == len(calvals) == len(self.soil_stack):
            for key in self.soil_stack:
                if len(self.soil_stack[key]) < 5:
                    return False
                else:
                    last_five = self.soil_stack[key][::-1][:5]
                    sensor_needs_watering = True
                    calval = None
                    if str(key) in calvals:
                        calval = calvals[str(key)]['median']
                    if calval is None:
                        return False
                    for val in last_five:
                        if val <= calval:
                            sensor_needs_watering = False
                            break
                    if sensor_needs_watering:
                        total_above_threshold+=1
            return total_above_threshold/len(self.soil_stack) >= 0.75
        else:
            return False

    def read_sensors(self):
        all_readings = {}
        for i in range(5):
            if self.loop is False:
                all_readings = {}
                break
            readings = sensors.soilsensor.read(values.DEBUG)
            for x in range(len(readings)):
                r = readings[x]
                if r["pin"] not in all_readings:
                    all_readings[r["pin"]] = []
                all_readings[r["pin"]].append(r["value"])
            time.sleep(1)
        return all_readings

    def throw_fakes(self, all_readings):
        true_readings = []
        for key in all_readings:
            fake_reading = False
            for val in all_readings[key]:
                if val == -1:
                    fake_reading = True
                    break
            if not fake_reading:
                median = statistics.median(all_readings[key])
                true_readings.append({"pin": key, "value": median})
        return true_readings

    def stack_readings(self, true_readings):
        soilchannels = values.values()["soil_sensor_channels"]
        if len(true_readings) == len(soilchannels):
            for kp in true_readings:
                if str(kp["pin"]) not in self.soil_stack:
                    self.soil_stack[str(kp["pin"])] = []
                self.soil_stack[str(kp["pin"])].append(kp["value"])
            for key in self.soil_stack:
                if len(self.soil_stack[key]) > 50:
                    self.soil_stack[key].pop(0)

    def run(self):
        start_recording_soil = time.time()
        start_taking_soil = 0
        while(self.loop):
            try:
                if time.time()-start_taking_soil >= 30:
                    start_taking_soil = time.time()
                    all_readings = self.read_sensors()
                    true_readings = self.throw_fakes(all_readings)
                    self.stack_readings(true_readings)
                    values.set_value(["current_soil", true_readings])

                    if time.time()-start_recording_soil >= 60:
                        start_recording_soil = time.time()
                        for i in range(len(true_readings)):
                            r = true_readings[i]
                            data.save_soil(r["pin"], r["value"])

                time.sleep(1)
            except Exception:
                if values.DEBUG:
                    traceback.print_exc()

        self.on_end()

########################################################################################################################
########################################################################################################################
########################################################################################################################

class TempWatch(Watch):
    def __init__(self):
        Watch.__init__(self)

    def on_end(self):
        pass

    def run(self):
        start_recording_temp = time.time()
        start_taking_temp = 0
        while(self.loop):
            try:
                if time.time()-start_taking_temp >= 10:
                    start_taking_temp = time.time()
                    #readings = sensors.thsensor.read(values.DEBUG)
                    readings = sensors.tpprobes.read(values.DEBUG)
                    totaltemp = 0
                    length = 0
                    for i in range(len(readings)):
                        temp = readings[i]["temp"]
                        if temp is not -1 and temp is not None:
                            totaltemp+=temp
                            length+=1
                    if totaltemp > 0 and length > 0:
                        temperature = totaltemp/length
                        values.set_value(["current_temp", temperature])
                        if time.time()-start_recording_temp >= 60:
                            start_recording_temp = time.time()
                            data.save_temp(temperature)
                    else:
                        values.set_value(["current_temp", None])

                time.sleep(1)
            except Exception:
                if values.DEBUG:
                    traceback.print_exc()

        self.on_end()

########################################################################################################################
########################################################################################################################
########################################################################################################################

class WaterWatch(Watch):
    def __init__(self):
        Watch.__init__(self)
        self.level_stack = []

    def on_end(self):
        pass

    def reservoir_has_water(self):
        if len(self.level_stack) < 10:
            return False
        last_ten = self.level_stack[::-1][:10]
        for val in last_ten:
            if val > 10000:
                return False
        return True

    def stack_reading(self, reading):
        self.level_stack.append(reading)
        if len(self.level_stack) > 50:
            self.level_stack.pop(0)

    def run(self):
        start_taking_level = 0
        while(self.loop):
            try:
                if time.time()-start_taking_level >= 5:
                    start_taking_level = time.time()
                    readings = sensors.wlsensor.read(values.DEBUG)
                    if len(readings) > 0:
                        self.stack_reading(readings[0]["value"])
                        values.set_value(["current_water_level", readings[0]["value"]])

                time.sleep(1)
            except Exception:
                if values.DEBUG:
                    traceback.print_exc()

########################################################################################################################
########################################################################################################################
########################################################################################################################

class CameraWatch(Watch):
    def __init__(self):
        Watch.__init__(self)

    def on_end(self):
        pass

    def run(self):
        start = time.time()
        while(self.loop):
            try:
                if values.values()["cameras_enabled"] is True:
                    mt = values.values()["morning_time"]
                    nt = values.values()["night_time"]
                    now = datetime.datetime.now()

                    day_times, night_times = util.time_ranges(mt, nt)

                    if day_times is not None and night_times is not None:
                        if now.hour in day_times:
                            if (time.time()-start) >= values.values()["image_interval"]*60:
                                start = time.time()
                                sensors.cameras.activate(values.DEBUG)
                        else:
                            start = 0

                time.sleep(1)
            except Exception:
                if values.DEBUG:
                    traceback.print_exc()

        self.on_end()
