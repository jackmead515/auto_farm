import os
import subprocess
import sys
import re

multi_stnr = re.compile('(\s|\t|\r|\n)+')
fswebcam_string = 'sudo fswebcam --quiet --no-title --no-timestamp --no-banner --deinterlace --png 9 -r 1024x768 -d '

def get_usb_cameras():
    output = os.popen('ls /dev/ | grep video').read()
    cameras = re.sub(multi_stnr, ' ', output).strip(' ').split()
    for i, camera in enumerate(cameras):
        cameras[i] = '/dev/' + camera
    return cameras

def snap_photo(camera, directory, image_name):
    if os.path.isdir(directory):
        path = os.path.join(directory, image_name)
        if not os.path.isfile(path):
            subprocess.run(fswebcam_string + camera + ' ' + path, shell=True)
            if os.path.isfile(path):
                return path
            else:
                return None
        else:
            return None
    else:
        return None
