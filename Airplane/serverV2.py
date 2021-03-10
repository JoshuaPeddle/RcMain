import sys
import os
sys.path.append((os.path.abspath(os.getcwd())))
import time
import struct
import board
import digitalio
from videoCapture import VideoStream
try:
    from nrf24.nrf import NRF
except:
    from nrf24 import nrf

# initialize the nRF24L01 on the spi bus object
nrf = NRF(0)

#nrf.pa_level = -12 # Set the PA. high(0,-6,-12,-18)low
#nrf.data_rate = 2  # Set the data transmission rate. (2,1)2Mbps,1Mbps
#nrf.channel = 125  # [0, 125]  [2.4, 2.525] GHz


video_stream = VideoStream()
payload = video_stream.get_frame()

print(nrf.print_details())
def master(count=20000):  # count = 5 will only transmit 5 packets
    """Transmits an incrementing integer every second"""
    nrf.listen = False  # ensures the nRF24L01 is in TX mode

    while count:
        payload = b'y'
        buffer = struct.pack("<f", payload)# "<f" means a single little endian (4 byte) float value.
        #split_payload=[payload[i:i + 32] for i in range(0, len(payload), 32)]
        #payload = [struct.pack("p", payload) for payload in split_payload]
        start_timer = time.monotonic_ns()  # start timer
        result = nrf.send(b'y')
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
        time.sleep(1)
        count -= 1


def video_stream2(count=200):
    """Transmits a videostream"""
    nrf.listen = False  # ensures the nRF24L01 is in TX mode
    import struct
    while count:
        payload = video_stream.get_frame()
        #print(payload)
        split_payload = [payload[i:i + 32] for i in range(0, len(payload), 32)]
        #struct.pack("=H", bytes(split_payload))
        # buffer = struct.pack("p", payload)
        print(len(split_payload))
        start_timer = time.monotonic_ns()  # start timer

        for load in split_payload:
            result = False
            while not result:
                result =nrf.send(load)
            #print(result)
            time.sleep(.0001)
        result = False
        time.sleep(.001)
        while not result:
            result = nrf.send(b'y')

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
        time.sleep(.01)

t = time.time()
#master()
video_stream2()
print('time to finish: '+str(time.time()-t))
