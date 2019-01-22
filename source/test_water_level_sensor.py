import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

def normalize(value):
    if value < 0.5:
        return 1
    else:
        return 0

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D25)
mcp = MCP.MCP3008(spi, cs)
channel4 = AnalogIn(mcp, MCP.P4)

while True:
    print('Voltage: ' + str(channel4.voltage))
    print('Normalize: ' + str(normalize(channel4.voltage)))
    print('-'*100)
    time.sleep(2)
