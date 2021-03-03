import serial   # use the serial module

import time     # delay functions

def test():

    ser = serial.Serial('COM3', 115200, timeout=1) #Change the COM PORT NUMBER to match your device
    if ser.isOpen():    # make sure port is open
        print(ser.name + ' open…')
    ser.write(b"yeet")
    while True:
        read = ser.read_all()
        decode = read.decode('utf-8')
        if decode == '':
            #time.sleep(0.001)
            continue
        print(decode)
        print("decode")
while True:
    try:
        test()
    except:
         #time.sleep(0.001)
         continue
