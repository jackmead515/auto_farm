import os
import glob
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
devices = glob.glob(base_dir + '28*')

def read_temp_raw(dfile):
    f = open(dfile, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp(dfile):
    lines = read_temp_raw(dfile)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(dfile)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

while True:
    readings = []
    for device in devices:
        dfile = device + '/w1_slave'
        readings.append(read_temp(dfile))
    print(readings)
    time.sleep(1)
