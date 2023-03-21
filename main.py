import json
import paho.mqtt.client as mqtt
import sqlite3
from time import time
import datetime #

a = currentDateTime = datetime.datetime.now() #
# a = str(currentDateTime)
# aevsis123 wifi
MQTT_HOST = '10.0.0.2' #raspberrypi.local / 10.0.0.2
MQTT_PORT = 1883
MQTT_CLIENT_ID = 'Python MQTT client'
MQTT_USER = 'YOUR MQTT USER'
MQTT_PASSWORD = 'YOUR MQTT USER PASSWORD'
TOPIC = '#' # nspanel-demo/sensor/demo_nspanel_temperature/state # paradox/states/zones/kontak/open
#TOPIC2 = 'nspanel-demo/sensor/demo_nspanel_temperature/state' #

DATABASE_FILE = 'mqtt.db'

def on_connect(mqtt_client, user_data, flags, conn_result):
    mqtt_client.subscribe(TOPIC)
    #mqtt_client.subscribe(TOPIC2)

def on_message(mqtt_client, user_data, message):
    print(message.payload.decode('utf-8'))
    payload = message.payload.decode('utf-8')

    db_conn = user_data['db_conn']
    # sql = 'INSERT INTO raspberry_data (topic, payload, time) VALUES (?, ?, ?)'
    sql = 'INSERT INTO raspberry_data (topic, payload, time) VALUES (?, ?, datetime("now", "localtime"))'
    cursor = db_conn.cursor()
    cursor.execute(sql, (message.topic, payload)) # a buraya
    db_conn.commit()
    cursor.close()


def main():
    db_conn = sqlite3.connect(DATABASE_FILE)
    sql = """
    CREATE TABLE IF NOT EXISTS raspberry_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        payload TEXT NOT NULL,
        time DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """
    # sql = """
    # CREATE TABLE IF NOT EXISTS raspberry_data (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     topic TEXT NOT NULL,
    #     payload TEXT NOT NULL,
    #     created_at INTEGER NOT NULL
    # )
    # """

    ### 2. database
    # sql2 = """
    # CREATE TABLE IF NOT EXISTS temperature (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     topic TEXT NOT NULL,
    #     payload TEXT NOT NULL,
    #     temperature TEXT NOT NULL,
    #     time DATETIME DEFAULT CURRENT_TIMESTAMP
    # )
    # """
    ###

    cursor = db_conn.cursor()
    cursor.execute(sql)
    # cursor.execute(sql2)# 2. database saved
    cursor.close()

    mqtt_client = mqtt.Client(MQTT_CLIENT_ID)
    # mqtt_client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    mqtt_client.user_data_set({'db_conn': db_conn})

    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_forever()

main()