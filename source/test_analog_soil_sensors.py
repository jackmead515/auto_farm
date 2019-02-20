import time
import busio
import digitalio
import board
import statistics as stats
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D25)
mcp = MCP.MCP3008(spi, cs)
channel0 = AnalogIn(mcp, MCP.P0)
channel1 = AnalogIn(mcp, MCP.P1)
channel2 = AnalogIn(mcp, MCP.P2)
channel3 = AnalogIn(mcp, MCP.P3)

while True:
    v0 = channel0.value
    v1 = channel1.value
    v2 = channel2.value
    v3 = channel3.value

    #print('Voltage: ' + str(round(channel0.voltage, 4)) + ', ' + str(round(channel1.voltage, 4)) + ', ' + str(round(channel2.voltage, 4)) + ', ' + str(round(channel3.voltage, 4)) + ', ')
    print(str(v0)+','+str(v1)+','+str(v2)+','+str(v3))
    time.sleep(2)
