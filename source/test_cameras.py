import time
import os
import psycopg2 as sql

import usb_controller as usb

cameras = usb.get_usb_cameras()

for camera in cameras:
    name = os.path.basename(camera) + '_' + str(round(time.time())) + '.png'
    image = usb.snap_photo(camera, '/home/pi/', name)
    if image is not None:
        print(camera + ' took image: ' + name)

        image_data = open(image, 'rb').read()

        try:
            dbname = "host='192.168.1.16' dbname='postgres' user='postgres'"
            c = sql.connect(dbname)
            db = c.cursor()
            try:
                db.execute('''
                INSERT INTO images (name, data) VALUES (%s, %s)
                ''', (name, sql.Binary(image_data)))
                c.commit()
            except:
                print("failed to upload " + name + " to database")
            finally:
                c.close()
        except:
            print("failed to connect to database")


        print(name + " uploaded to database")
