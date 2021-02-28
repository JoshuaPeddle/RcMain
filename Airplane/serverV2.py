
import time
import struct
import board
import digitalio

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

def test():
    import numpy as np
    arr = np.zeros([1, 3])
    payload= arr.tobytes()
    print(len(payload))
    return payload
payload = test()

from videoCapture import VideoStream
video_stream = VideoStream()
payload = video_stream.get_frame()
# nrf.allow_ask_no_ack = False
# nrf.dynamic_payloads = False
# nrf.payload_length = 4

print(nrf.print_details())
def master(count=20):  # count = 5 will only transmit 5 packets
    """Transmits an incrementing integer every second"""
    nrf.listen = False  # ensures the nRF24L01 is in TX mode

    while count:
        #payload = video_stream.get_frame()
        #print('cx')
        # use struct.pack to packetize your data
        # into a usable payload
        #buffer = struct.pack("<f", payload)
        split_payload=[payload[i:i + 32] for i in range(0, len(payload), 32)]
        #buffer = struct.pack("p", payload)
        #print(buffer)
        #payload = [struct.pack("p", payload) for payload in split_payload]
        #print(payload)
        # "<f" means a single little endian (4 byte) float value.
        start_timer = time.monotonic_ns()  # start timer
        result = nrf.send(split_payload)
        end_timer = time.monotonic_ns()  # end timr
        if not result:
            print("send() failed or timed out")
        else:
            print(
                "Transmission successful! Time to Transmit: "
                "{} us. Sent: {}".format(
                    (end_timer - start_timer) / 1000, '!S'
                )
            )
        #payload[0] += 0.01
        #time.sleep(0.01)
        count -= 1

def video_stream(count=20):
  """Transmits a videostream"""
    nrf.listen = False  # ensures the nRF24L01 is in TX mode

    while count:
        payload = video_stream.get_frame()
        split_payload=[payload[i:i + 32] for i in range(0, len(payload), 32)]
        #buffer = struct.pack("p", payload)
        print(len(split_payload))
        #payload = [struct.pack("p", payload) for payload in split_payload]
        #print(payload)
        # "<f" means a single little endian (4 byte) float value.
        start_timer = time.monotonic_ns()  # start timer
        result = nrf.send(split_payload)
        end_timer = time.monotonic_ns()  # end timr
        if not result:
            print("send() failed or timed out")
        else:
            print(
                "Transmission successful! Time to Transmit: "
                "{} us. Sent: {}".format(
                    (end_timer - start_timer) / 1000, '!S'
                )
            )
        time.sleep(2)
        count -= 1


t = time.time()
master()
print('time to finish: '+str(time.time()-t))
