import time
import os
import subprocess

import usb_controller as usb

cameras = usb.get_usb_cameras()
for camera in cameras:
    name = os.path.basename(camera) + '_' + str(round(time.time())) + '.jpg'
    image = usb.snap_photo(camera, '/home/pi/', name)
    if image is not None:
        print(camera + ' took image: ' + name)
        #move image to somewhere!
