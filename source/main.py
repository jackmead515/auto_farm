
from api import app
import watch
import gpio_controller as gpio
import values
import data
import sensors

if __name__ == '__main__':

    print("Initializing constants...")
    values.initialize()

    print("Initializing database...")
    data.initialize()

    print("Initializing pins...")
    gpio.initialize()

    print("Initializing sensors...")
    sensors.initialize()

    print("Starting main loop...")
    watch.initialize()
    watch.start()

    print("Start web app...")
    app.run(host='0.0.0.0', port=80, debug=False)
