import Adafruit_DHT

pins = [15, 18]

def read_tphd_sensors():
    readings = []
    for pin in pins:
        #readings.append(4);
        humid, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
        readings.append({"humid": humid, "temp": temp})
    return readings

print(read_tphd_sensors())
