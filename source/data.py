import datetime
import uuid
import sqlite3 as sql

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
    db.execute("SELECT * FROM notifications")
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
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data

def save_soil(value):
    idd = str(uuid.uuid4())
    connection = sql.connect("../db/database.db")
    db = connection.cursor()
    db.execute("INSERT INTO soil (id, ctime, value) VALUES (?, ?, ?)", (idd, datetime.datetime.now(), value))
    connection.commit()
    connection.close()

def get_soil():
    connection = sql.connect("../db/database.db")
    db = connection.cursor()

    db.execute('''
    SELECT * FROM soil
    WHERE DATETIME(soil.ctime) >= (?)
    AND DATETIME(soil.ctime) <= (?)
    ''', [(start), (end)])

    db.execute("SELECT * FROM soil")
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
    ''', [(start), (end)])

    data = db.fetchall()
    connection.commit()
    connection.close()
    return data
