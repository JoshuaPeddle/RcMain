import time
import struct
import board
import digitalio
import base64
import numpy as np
import cv2
# if running this on a ATSAMD21 M0 based board
# from circuitpython_nrf24l01.rf24_lite import RF24
from circuitpython_nrf24l01.rf24 import RF24

# we'll be using the dynamic payload size feature (enabled by default)
# Wiring
ce = digitalio.DigitalInOut(board.D22)
csn = digitalio.DigitalInOut(board.D8)
spi = board.SPI()  # spi grabbed from board class

# initialize the nRF24L01 on the spi bus object
nrf = RF24(spi, csn, ce)
nrf.pa_level = -12 # Set the PA. high(0,-6,-12,-18)low
nrf.data_rate = 2  # Set the data transmission rate. (2,1)2Mbps,1Mbps
nrf.channel = 125  # [0, 125]  [2.4, 2.525] GHz

# addresses needs to be in a buffer protocol object (bytearray)
address = [b"1Node", b"2Node"]
radio_number = bool(0)
# set TX address of RX node into the TX pipe
nrf.open_tx_pipe(address[radio_number])  # always uses pipe 0
# set RX address of TX node into an RX pipe
nrf.open_rx_pipe(1, address[not radio_number])  # using pipe 1

# uncomment the following 3 lines for compatibility with TMRh20 library
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
            # grab information about the received payload
            payload_size, pipe_number = (nrf.any(), nrf.pipe)
            # fetch 1 payload from RX FIFO
            buffer = nrf.read()  # also clears nrf.irq_dr status flag
            #print(buffer)
            print(
                "Received {} bytes on pipe {}: {}".format(
                    payload_size, pipe_number, buffer
                )
            )
            start = time.monotonic()
    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode
def video_client(timeout=60):
    """Polls the radio and prints the received value. This method expires
    after 6 seconds of no received transmission"""
    nrf.listen = True  # put radio into RX mode and power up

    start = time.monotonic()
    while (time.monotonic() - start) < timeout:
        if nrf.available():
            # grab information about the received payload
            payload_size, pipe_number = (nrf.any(), nrf.pipe)
            # fetch 1 payload from RX FIFO
            buffer = nrf.read()  # also clears nrf.irq_dr status flag
            try:

                img = base64.b64decode(buffer)
                npimg = np.fromstring(img, dtype=np.uint8)
                source = cv2.imdecode(npimg, 1)
                cv2.imshow("Stream", source)
                cv2.waitKey(1)

            except KeyboardInterrupt:
                cv2.destroyAllWindows()
                break
            #print(buffer)
            print(
                "Received {} bytes on pipe {}: {}".format(
                    payload_size, pipe_number, buffer
                )
            )
            start = time.monotonic()
    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode
client()