import json
import argparse
import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

sensor_values = {'values': [], 'voltages': []}

parser = argparse.ArgumentParser(description='Record soil moisture over time')
parser.add_argument('--mins', dest='total_mins', type=int, nargs='?',
                   help='amount of mintues to record soil moisture values')
parser.add_argument('--interval', dest='interval', type=int, nargs='?',
                   help='sample rate of the moisture sensors')

args = parser.parse_args()

total_mins = args.total_mins
interval = args.interval

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D25)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.P0)
channel1 = AnalogIn(mcp, MCP.P1)
channel2 = AnalogIn(mcp, MCP.P2)
channel3 = AnalogIn(mcp, MCP.P3)

print('Recording started...')

start = time.time()
while True:
    if time.time()-start > total_mins*60:
        break
    else:
        v1 = channel0.voltage
        v2 = channel1.voltage
        v3 = channel2.voltage
        v4 = channel3.voltage
        a1 = channel0.value
        a2 = channel1.value
        a3 = channel2.value
        a4 = channel3.value
        sensor_values['voltages'].append({'pin': 0, 'val': v1})
        sensor_values['voltages'].append({'pin': 1, 'val': v2})
        sensor_values['voltages'].append({'pin': 2, 'val': v3})
        sensor_values['voltages'].append({'pin': 3, 'val': v4})
        sensor_values['values'].append({'pin': 0, 'val': a1})
        sensor_values['values'].append({'pin': 1, 'val': a2})
        sensor_values['values'].append({'pin': 2, 'val': a3})
        sensor_values['values'].append({'pin': 3, 'val': a4})
    time.sleep(interval)

print('Recording ended...')

with open('data.json', 'w+') as f:
    json.dump(sensor_values, f)

print('Data saved!')
