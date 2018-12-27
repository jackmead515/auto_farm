import os
import subprocess
import sys
import re

multi_stnr = re.compile('(\s|\t|\r|\n)+')

def get_usb_cameras():
    output = os.popen('ls /dev/ | grep video').read()
    cameras = re.sub(multi_stnr, ' ', output).strip(' ').split()
    for camera in cameras:
        camera = '/dev/' + camera
    return cameras

def power_on_usb():
    output = os.popen('sudo ./hub-ctrl -h 0 -P 2 -p 1').read()

def power_off_usb():
    output = os.popen('sudo ./hub-ctrl -h 0 -P 2 -p 0').read()

def snap_photo(camera, directory, image_name):
    if os.path.isdir(directory):
        path = os.path.join(directory, image_name)
        if not os.path.isfile(path):
            subprocess.call('sudo fswebcam --quiet --no-info --no-title --no-timestamp --no-banner --deinterlace --png -r 1024x768 -d ' + camera + ' ' + path, shell=True, stdout=subprocess.PIPE)
            if os.path.isfile(path):
                return path
            else:
                return None
        else:
            return None
    else:
        return None
