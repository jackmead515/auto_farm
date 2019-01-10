import threading
import time
import datetime

import values
import data
import util
import sensors

def start():
    threading.Thread(target=read_temperature_probes).start()
    threading.Thread(target=watch_cameras).start()
    threading.Thread(target=watch_lights).start()
    threading.Thread(target=watch_heat).start()
    #threading.Thread(target=watch_soil).start()

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
    start = time.time()
    while(True):
        try:
            readings = sensors.soilsensor.read(values.DEBUG)

            total = 0
            for i in range(len(readings)):
                data.save_soil(readings[i]["pin"], readings[i]["value"])
                if readings[i]["value"] <= values.values()["soil_sensor_limit"]:
                    total+=1

            if total/len(readings) >= 0.75 and (time.time()-start) >= values.values()["pump_interval"]:
                start = time.time()
                data.save_pump()
                sensors.pump.activate(values.DEBUG)

            time.sleep(values.values()["soil_interval"])
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
