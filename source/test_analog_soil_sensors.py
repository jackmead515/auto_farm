import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

def normalize(value):
    if value < 1 or round(value) <= 0:
        return -1
    else:
        normalized = int((100 - (value * 100 / 3.3))*2)
        if normalized < 0:
            normalized = 0
        if normalized > 100:
            normalized = 100
        return normalized

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D25)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.P0)
channel1 = AnalogIn(mcp, MCP.P1)
channel2 = AnalogIn(mcp, MCP.P2)
channel3 = AnalogIn(mcp, MCP.P3)

while True:
    print('Voltage: ' + str(channel0.voltage) + 'V, ' + str(channel1.voltage) + 'V, ' + str(channel2.voltage) + 'V, ' + str(channel3.voltage) + 'V, ')
    print('Normalized (0-100): ' + str(normalize(channel0.voltage)) + ', ' + str(normalize(channel1.voltage)) + ', ' + str(normalize(channel2.voltage)) + ', ' + str(normalize(channel3.voltage)) + ', ')
    print('-'*100)
    time.sleep(2)
