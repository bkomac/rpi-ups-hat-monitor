import struct
import smbus
import sys
import time
import paho.mqtt.client as mqtt
import os
import json
import socket


def readVoltage(bus):
    "This function returns as float the voltage from the Raspi UPS Hat via the provided SMBus object"
    address = 0x36
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = round(swapped * 78.125 / 1000000, 2)
    return voltage


def readCapacity(bus):
    "This function returns as a float the remaining capacity of the battery connected to the Raspi UPS Hat via the provided SMBus object"
    address = 0x36
    read = bus.read_word_data(address, 4)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped/256
    return capacity


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("sensor/iopi/ports")


def on_message(client, userdata, msg):
    message = str(msg.payload)
    print(msg.topic+" "+message)


def on_publish(mosq, obj, mid):
    print("mid: " + str(mid))

#password = os.environ.get('MQTT_PASS')

with open("password.txt") as f:
    lines = f.readlines()
    username = lines[0].strip()
    password = lines[1].strip()
    print(f"USERNAME={username}, PASSWORD={password}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username, password)
client.connect("node.komac.si", 11883, 60)
client.loop_start()

bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)

print("Voltage:%5.2fV" % readVoltage(bus))

print("Battery:%5i%%" % readCapacity(bus))


# draw battery

n = int(round(readCapacity(bus) / 10))

print("----------- ")

sys.stdout.write('|')

for i in range(0, n):

    sys.stdout.write('#')

for i in range(0, 10-n):

    sys.stdout.write(' ')

sys.stdout.write('|+\n')

print("----------- ")


if readCapacity(bus) == 100:

    print("Battery FULL")

if readCapacity(bus) < 20:

    print("Battery LOW")


while True:
    sensor_data = json.dumps({"voltage": readVoltage(bus), "percent": readCapacity(bus), "host": socket.gethostname()})
    print("Voltage:%5.2fV" % readVoltage(bus))

    print("Battery:%5i%%" % readCapacity(bus))
    client.publish("pi05/ups", sensor_data)
    time.sleep(10)
