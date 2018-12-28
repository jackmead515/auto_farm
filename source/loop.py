import threading
import time
import datetime

import values
import data
import util
import sensors

########################################################################################################################
def watch_lights():
    while(True):
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

########################################################################################################################
def watch_soil():
    start = time.time()
    while(True):

        readings = sensors.soilsensor.read(values.DEBUG)

        total = 0
        if values.values()["soil_sensor_type"] == 'digital':
            for i in range(len(readings)):
                if readings[i]["value"] == 1:
                    total+=1
        elif values.values()["soil_sensor_type"] == 'analog':
            for i in range(len(readings)):
                if readings[i]["value"] <= values.values()["analog_soil_sensor_limit"]:
                    total+=1

        if total/len(readings) >= 0.75 and (time.time()-start) >= values.values()["pump_interval"]:
            start = time.time()
            data.save_soil(1)
            data.save_pump()
            sensors.pump.activate(values.DEBUG)

        time.sleep(values.values()["soil_interval"])

########################################################################################################################
def watch_heat():
    while(True):

        readings = sensors.thsensor.read(values.DEBUG)

        totalhumid = 0
        totaltemp = 0
        length = 0
        for i in range(len(readings)):
            if readings[i]["humid"] is None or readings[i]["temp"] is None:
                data.save_message(
                    "Invalid TH Reading",
                    "Sensor on pin: " + str(readings[i]["pin"]) + " reported an invalid result. This sensor may be broken."
                )
            else:
                length+=1
                totaltemp+=readings[i]["temp"]
                totalhumid+=readings[i]["humid"]

        if totalhumid > 0 and length > 0:
            averagehumid = totalhumid/length
            data.save_humid(averagehumid)

        if totaltemp > 0 and length > 0:
            average = totaltemp/length

            data.save_temp(average)

            mt = values.values()["morning_time"]
            nt = values.values()["night_time"]
            now = datetime.datetime.now()

            day_times, night_times = util.time_ranges(mt, nt)

            if day_times is not None and night_times is not None:
                if now.hour in day_times:
                    if average >= values.values()["day_temp"] and values.status()["heatlights"] is True:
                        data.save_heat(0)
                        sensors.heatlights.deactivate(values.DEBUG)
                    elif average < values.values()["day_temp"] and values.status()["heatlights"] is False:
                        data.save_heat(1)
                        sensors.heatlights.activate(values.DEBUG)
                elif now.hour in night_times:
                    if average >= values.values()["night_temp"] and values.status()["heatlights"] is True:
                        data.save_heat(0)
                        sensors.heatlights.deactivate(values.DEBUG)
                    elif average < values.values()["night_temp"] and values.status()["heatlights"] is False:
                        data.save_heat(1)
                        sensors.heatlights.activate(values.DEBUG)

        time.sleep(values.values()["tphd_interval"])

########################################################################################################################
def watch_cameras():
    while(True):

        mt = values.values()["morning_time"]
        nt = values.values()["night_time"]
        now = datetime.datetime.now()

        day_times, night_times = util.time_ranges(mt, nt)

        if day_times is not None and night_times is not None:
            if now.hour in day_times:
                sensors.cameras.activate(values.DEBUG)

        time.sleep(values.values()["image_interval"])


########################################################################################################################
def start():
    threading.Thread(target=watch_cameras).start()
    threading.Thread(target=watch_lights).start()
    threading.Thread(target=watch_heat).start()
    threading.Thread(target=watch_soil).start()
