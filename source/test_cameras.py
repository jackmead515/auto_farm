import time
import os
import psycopg2 as sql

import usb_controller as usb

cameras = usb.get_usb_cameras()

for camera in cameras:

    name = os.path.basename(camera) + '_' + str(round(time.time())) + '.png'
    path = usb.snap_photo(camera, '/home/pi/auto_farm/images/', name)

    if path is not None:
        print(camera + ' took image: ' + name)
