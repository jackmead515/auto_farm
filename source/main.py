
from api import app
import loop
import gpio_controller as gpio
import values
import data
import sensors

if __name__ == '__main__':

    print("Initializing constants...")
    values.initalize()
    values.load()

    print("Initializing database...")
    data.initialize()

    print("Initializing pins...")
    gpio.initialize()

    print("Initializing sensors...")
    sensors.initalize()
    sensors.buzzer.activate("start", 1, values.DEBUG)

    print("Starting main loop...")
    loop.start()

    print("Start web app...")
    app.run(host='0.0.0.0', port=80, debug=False)
