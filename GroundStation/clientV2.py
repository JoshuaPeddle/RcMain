import time
#import struct
#import board
#import digitalio
import base64
import numpy as np
import cv2
import os
import sys
sys.path.append((os.path.abspath(os.getcwd())))
try:
    from nrf24.nrf import  NRF
except:
    from nrf24 import nrf


nrf = NRF(1)
#nrf.pa_level = -12 # Set the PA. high(0,-6,-12,-18)low
#nrf.data_rate = 2  # Set the data transmission rate. (2,1)2Mbps,1Mbps
#nrf.channel = 125  # [0, 125]  [2.4, 2.525] GHz


def client(timeout=60):
    """Polls the radio and prints the received value. This method expires
    after 6 seconds of no received transmission"""
    nrf.listen = True  # put radio into RX mode and power up

    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        if nrf.available():
            payload_size, pipe_number = (nrf.any(), nrf.pipe)
            buffer = nrf.read(payload_size)  # also clears nrf.irq_dr status flag
            #print(buffer)
            start = time.monotonic()
    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode


def video_client_awk(timeout=60):
    """Polls the radio and prints the received value. This method expires
    after 6 seconds of no received transmission"""
    nrf.listen = True  # put radio into RX mode and power up
    payload = ''
    last = ''
    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        if nrf.available():
            payload_size, pipe_number = (nrf.any(), nrf.pipe)
            buffer= nrf.read(payload_size)
            if buffer != b'y':
                try:
                    dec = buffer.decode()
                except UnicodeDecodeError:
                    continue
                if dec != last:
                    last = dec
                    payload = payload + dec
            else:
                try:

                    img = base64.b64decode(payload.strip())
                    npimg = np.fromstring(img, dytpe=np.uint8)
                    source = cv2.imdecode(npimg, flags=cv2.IMREAD_ANYCOLOR)
                    source = cv2.resize(source, (600,400))
                    #cv2.imshow("Stream", source)
                    #cv2.waitKey(500)
                    #time.sleep(0.001)
                    #cv2.destroyWindow("Stream")
                    print('successfull transmission')
                    payload = ''
                except:
                    payload= ''
                    print('failed frame')
            nrf.listen = False
            result = False
            while not result:
                result = nrf.send(b'a')
            nrf.listen = True
            start = time.monotonic()
    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode



def video_client_noawk(timeout=60):
    """Polls the radio and prints the received value. This method expires
    after 6 seconds of no received transmission"""
    nrf.listen = True  # put radio into RX mode and power up
    payload = ''
    last = ''
    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        if nrf.available():
            payload_size, pipe_number = (nrf.any(), nrf.pipe)
            buffer= nrf.read(payload_size)
            if buffer != b'y':
                try:
                    dec = buffer.decode()
                except UnicodeDecodeError:
                    continue
                if dec != last:
                    last = dec
                    payload = payload + dec
            else:
                try:
                    source = cv2.imdecode(np.fromstring(base64.b64decode(payload.strip()), dtype=np.uint8), 1)
                    #cv2.imshow("Stream", source)
                    #cv2.waitKey(1000)
                    #time.sleep(0.001)
                    #cv2.destroyWindow("Stream")
                    print('successfull transmission')
                    payload = ''
                except:
                    payload= ''
                    print('failed frame')

            start = time.monotonic()
    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode
if __name__ == "__main__":
    userSel = input('0: client, 1: video_client')
    runnables = {'0':client, '1':video_client_awk}
    runnables[userSel]()
