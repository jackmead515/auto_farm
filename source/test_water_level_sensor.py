import time
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
cs = digitalio.DigitalInOut(board.D25)
mcp = MCP.MCP3008(spi, cs)
channel4 = AnalogIn(mcp, MCP.P4)

while True:
    print('Value: ' + str(channel4.value))
    print('-'*100)
    time.sleep(2)
