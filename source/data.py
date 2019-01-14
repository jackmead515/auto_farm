import datetime
import uuid
import base64
import sqlite3 as sql
import psycopg2 as postsql

import values

def initialize():
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    CREATE TABLE IF NOT EXISTS notifications (
        id VARCHAR(255) NOT NULL,
        ctime TIMESTAMP NOT NULL,
        title VARCHAR(255) NOT NULL,
        message TEXT NOT NULL
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS temperature (
        id VARCHAR(255) NOT NULL,
        ctime TIMESTAMP NOT NULL,
        value DOUBLE NOT NULL
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS humidity (
        id VARCHAR(255) NOT NULL,
        ctime TIMESTAMP NOT NULL,
        value DOUBLE NOT NULL
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS soil (
        id VARCHAR(255) NOT NULL,
        ctime TIMESTAMP NOT NULL,
        pin INT NOT NULL,
        value INT NOT NULL
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS lights (
        id VARCHAR(255) NOT NULL,
        ctime TIMESTAMP NOT NULL,
        value INT NOT NULL
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS heat (
        id VARCHAR(255) NOT NULL,
        ctime TIMESTAMP NOT NULL,
        value INT NOT NULL
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS pump (
        id VARCHAR(255) NOT NULL,
        ctime TIMESTAMP NOT NULL
    )
    ''')

    connection.commit()
    connection.close()

def save_message(title, message):
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO notifications (id, ctime, title, message) VALUES (?, ?, ?, ?)", (idd, datetime.datetime.now(), title, message))
    connection.commit()
    connection.close()

def get_messages():
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("SELECT * FROM notifications ORDER BY notifications.ctime ASC")
    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_pump():
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO pump (id, ctime) VALUES (?, ?)", (idd, datetime.datetime.now()))
    connection.commit()
    connection.close()

def get_pump():
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    SELECT * FROM pump
    WHERE DATETIME(pump.ctime) >= (?)
    AND DATETIME(pump.ctime) <= (?)
    ORDER BY pump.ctime ASC
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_lights(value):
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO lights (id, ctime, value) VALUES (?, ?, ?)", (idd, datetime.datetime.now(), value))
    connection.commit()
    connection.close()

def get_lights():
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    SELECT * FROM lights
    WHERE DATETIME(lights.ctime) >= (?)
    AND DATETIME(lights.ctime) <= (?)
    ORDER BY lights.ctime ASC
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_heat(value):
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO heat (id, ctime, value) VALUES (?, ?, ?)", (idd, datetime.datetime.now(), value))
    connection.commit()
    connection.close()

def get_heat(start, end):
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    SELECT * FROM heat
    WHERE DATETIME(heat.ctime) >= (?)
    AND DATETIME(heat.ctime) <= (?)
    ORDER BY heat.ctime ASC
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_soil(pin, value):
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO soil (id, ctime, pin, value) VALUES (?, ?, ?, ?)", (idd, datetime.datetime.now(), pin, value))
    connection.commit()
    connection.close()

def get_soil(start, end):
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    SELECT * FROM soil
    WHERE DATETIME(soil.ctime) >= (?)
    AND DATETIME(soil.ctime) <= (?)
    ORDER BY soil.ctime ASC
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_humid(value):
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO humidity (id, ctime, value) VALUES (?, ?, ?)", (idd, datetime.datetime.now(), value))
    connection.commit()
    connection.close()

def get_humid(start, end):
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    SELECT * FROM humidity
    WHERE DATETIME(humidity.ctime) >= (?)
    AND DATETIME(humidity.ctime) <= (?)
    ORDER BY humidity.ctime ASC
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_temp(value):
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO temperature (id, ctime, value) VALUES (?, ?, ?)", (idd, datetime.datetime.now(), value))
    connection.commit()
    connection.close()

def get_temp(start, end):
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    SELECT * FROM temperature
    WHERE DATETIME(temperature.ctime) >= (?)
    AND DATETIME(temperature.ctime) <= (?)
    ORDER BY temperature.ctime ASC
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_image(name, data):
    dbname = "host='" + values.values()["imagedb_host"] + "' dbname='postgres' user='postgres'"
    c = postsql.connect(dbname)
    db = c.cursor()
    db.execute('''
    INSERT INTO jack_images (name, data, ctime) VALUES (%s, %s, %s)
    ''', (name, postsql.Binary(data), datetime.datetime.now()))
    c.commit()
    c.close()

def get_images(index):
    dbname = "host='" + values.values()["imagedb_host"] + "' dbname='postgres' user='postgres'"
    c = postsql.connect(dbname)
    db = c.cursor()
    db.execute('''
    SELECT id, name, ctime FROM jack_images
    ORDER BY ctime DESC
    OFFSET %s LIMIT 50
    ''', [index])
    data = db.fetchall()
    c.commit()
    c.close()
    return data

def get_image(name):
    dbname = "host='" + values.values()["imagedb_host"] + "' dbname='postgres' user='postgres'"
    c = postsql.connect(dbname)
    db = c.cursor()
    db.execute('''
    SELECT data FROM jack_images WHERE jack_images.name = %s LIMIT 1
    ''', [name])
    data = db.fetchall()
    image = None
    if data[0] is not None:
        image = bytes.decode(base64.b64encode(data[0][0]))
    c.commit()
    c.close()
    return image
