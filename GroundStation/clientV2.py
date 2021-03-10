import time
import struct
import board
import digitalio
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


# initialize the nRF24L01 on the spi bus object
nrf = NRF()
nrf.pa_level = -12 # Set the PA. high(0,-6,-12,-18)low
nrf.data_rate = 2  # Set the data transmission rate. (2,1)2Mbps,1Mbps
nrf.channel = 125  # [0, 125]  [2.4, 2.525] GHz

# addresses needs to be in a buffer protocol object (bytearray)
address = [b"1Node", b"2Node"]
radio_number = bool(1)
# set TX address of RX node into the TX pipe
nrf.open_tx_pipe(address[radio_number])  # always uses pipe 0
# set RX address of TX node into an RX pipe
nrf.open_rx_pipe(1, address[not radio_number])  # using pipe 1

# uncomment the following 3 lines for compatibility with TMRh20 library++++++++
# nrf.allow_ask_no_ack = False
# nrf.dynamic_payloads = False
# nrf.payload_length = 4


def client(timeout=60):
    """Polls the radio and prints the received value. This method expires
    after 6 seconds of no received transmission"""
    nrf.listen = True  # put radio into RX mode and power up

    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        if nrf.available():
            #print('dd')
            # grab information about the received payload
            payload_size, pipe_number = (nrf.any(), nrf.pipe)
            # fetch 1 payload from RX FIFO
            buffer = nrf.read(payload_size)  # also clears nrf.irq_dr status flag
            #print(buffer)
            #print(
            #    "Received {} bytes on pipe {}: {}".format(
            #        payload_size, pipe_number, buffer
            #    )
            #)
            start = time.monotonic()
    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode
def video_client(timeout=60):
    """Polls the radio and prints the received value. This method expires
    after 6 seconds of no received transmission"""
    nrf.listen = True  # put radio into RX mode and power up
    payload = ''
    last = ''
    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        if nrf.available():

            # grab information about the received payload
            payload_size, pipe_number = (nrf.any(), nrf.pipe)
            # fetch 1 payload from RX FIFO
            # also clears nrf.irq_dr status flag
            buffer= nrf.read(payload_size)
            if buffer != b'y':
                try:
                    dec = buffer.decode()
                except:
                    continue
                if dec == last:
                    None
                else:
                    last = dec
                    payload= payload+dec
            else:
                try:

                    #print('payload = ' +str(payload))
                    #print(len(payload))
                    img = base64.b64decode(payload.strip())
                    #print(f'img    {img}')
                    npimg = np.fromstring(img, dtype=np.uint8)
                    #print(f'npimg    {npimg}')
                    source = cv2.imdecode(npimg, 1)
                    #print(f'source:   {source}')
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
video_client()