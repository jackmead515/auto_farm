import threading
import time
import datetime
import statistics

import values
import data
import util
import sensors

def start():
    threading.Thread(target=read_temperature_probes).start()
    threading.Thread(target=read_soil_sensors).start()
    threading.Thread(target=watch_cameras).start()
    threading.Thread(target=watch_lights).start()
    threading.Thread(target=watch_heat).start()
    threading.Thread(target=watch_soil).start()

########################################################################################################################
def read_temperature_probes():
    start_recording_temp = time.time()
    while(True):
        try:
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

            time.sleep(values.values()["tp_interval"])
        except Exception as e:
            print(e)

########################################################################################################################
def read_soil_sensors():
    start_recording_soil = time.time()
    while(True):
        try:

            all_readings = {}
            true_readings = []

            for i in range(5):
                readings = sensors.soilsensor.read(values.DEBUG)
                for x in range(len(readings)):
                    r = readings[x]
                    if r["pin"] not in all_readings:
                        all_readings[r["pin"]] = []
                    all_readings[r["pin"]].append(r["value"])
                time.sleep(1)

            for key in all_readings:
                fake_reading = False
                for val in all_readings[key]:
                    if val == -1:
                        fake_reading = True
                        break
                if not fake_reading:
                    median = statistics.median(all_readings[key])
                    true_readings.append({"pin": key, "value": median})

            values.set_value(["current_soil", true_readings])

            if time.time()-start_recording_soil >= 60:
                start_recording_soil = time.time()
                for i in range(len(true_readings)):
                    r = true_readings[i]
                    data.save_soil(r["pin"], r["value"])

            time.sleep(values.values()["soil_interval"])

        except Exception as e:
            print(e)

########################################################################################################################
def watch_lights():
    while(True):
        try:
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

            time.sleep(10)
        except Exception as e:
            print(e)

########################################################################################################################
def watch_soil():
    while(True):
        try:

            readings = values.values()["current_soil"]
            if len(readings) > 0:
                total_below_threshold = 0
                for i in range(len(readings)):
                    if readings[i]["value"] <= values.values()["soil_sensor_limit"]:
                        total_below_threshold+=1

                if total_below_threshold/len(readings) >= 0.75:
                    data.save_pump()
                    #sensors.pump.activate(values.DEBUG)

                time.sleep(values.values()["pump_interval"])
            else:
                time.sleep(10)

        except Exception as e:
            print(e)

########################################################################################################################
def watch_heat():
    while(True):
        try:
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
                        sensors.heatlights.activate(values.DEBUG)
                elif now.hour in night_times:
                    if values.values()["current_temp"] >= values.values()["night_temp"] and values.status()["heatlights"] is True:
                        data.save_heat(0)
                        sensors.heatlights.deactivate(values.DEBUG)
                    elif values.values()["current_temp"] < values.values()["night_temp"] and values.status()["heatlights"] is False:
                        data.save_heat(1)
                        sensors.heatlights.activate(values.DEBUG)

            time.sleep(1)
        except Exception as e:
            print(e)

########################################################################################################################
def watch_cameras():
    start = 0
    while(True):
        try:
            mt = values.values()["morning_time"]
            nt = values.values()["night_time"]
            now = datetime.datetime.now()

            day_times, night_times = util.time_ranges(mt, nt)

            if day_times is not None and night_times is not None:
                if now.hour in day_times:
                    if (time.time()-start) >= values.values()["image_interval"]:
                        start = time.time()
                        sensors.cameras.activate(values.DEBUG)
                else:
                    start = 0

            time.sleep(10)
        except Exception as e:
            print(e)

########################################################################################################################
