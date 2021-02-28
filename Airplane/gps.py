

import serial
import pynmea2

port = "/dev/serial0"


def parseGPS(s):
    s = str(s)[2:-5]
    if 'GGA' in s:
        msg = pynmea2.parse(s)
        print(
        "Timestamp: {} -- Lat: {} {} -- Lon: {} {} -- Altitude: {} {} -- Satellites: {}".format(
        msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units, msg.num_sats)
        )


serialPort = serial.Serial(port, baudrate=9600, timeout=0.5)
while True:
    s = serialPort.readline()
    try:
        parseGPS(s)
    except: None