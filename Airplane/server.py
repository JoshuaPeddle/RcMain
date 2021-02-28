
import time
import struct
import board
import digitalio

# if running this on a ATSAMD21 M0 based board
# from circuitpython_nrf24l01.rf24_lite import RF24
from circuitpython_nrf24l01.rf24 import RF24

# change these (digital output) pins accordingly
ce = digitalio.DigitalInOut(board.D22)
csn = digitalio.DigitalInOut(board.D8)

# using board.SPI() automatically selects the MCU's
# available SPI pins, board.SCK, board.MOSI, board.MISO
spi = board.SPI()  # init spi bus object

# we'll be using the dynamic payload size feature (enabled by default)
# initialize the nRF24L01 on the spi bus object
nrf = RF24(spi, csn, ce)

# set the Power Amplifier level to -12 dBm since this test example is
# usually run with nRF24L01 transceivers in close proximity
nrf.pa_level = -12

nrf.data_rate =2


# addresses needs to be in a buffer protocol object (bytearray)
address = [b"1Node", b"2Node"]

# to use different addresses on a pair of radios, we need a variable to
# uniquely identify which address this radio will use to transmit
# 0 uses address[0] to transmit, 1 uses address[1] to transmit
radio_number = bool(
    #int(input("Which radio is this? Enter '0' or '1'. Defaults to '0' ") or 0)
    0
)

# set TX address of RX node into the TX pipe
nrf.open_tx_pipe(address[radio_number])  # always uses pipe 0

# set RX address of TX node into an RX pipe
nrf.open_rx_pipe(1, address[not radio_number])  # using pipe 1

# using the python keyword global is bad practice. Instead we'll use a 1 item
# list to store our float number for the payloads sent
payload = [0.0]
#import numpy as np
#arr = np.zeros([1, 3])
#payload= arr.tobytes()
#print(len(payload))
#arr2 = np.zeros([20, 20])
#payload2= len(arr2.tobytes())
#print(payload2)
# uncomment the following 3 lines for compatibility with TMRh20 library
# nrf.allow_ask_no_ack = False
# nrf.dynamic_payloads = False
# nrf.payload_length = 4

print(nrf.print_details())
def master(count=0):  # count = 5 will only transmit 5 packets
    """Transmits an incrementing integer every second"""
    nrf.listen = False  # ensures the nRF24L01 is in TX mode

    while count:
        #print('cx')
        # use struct.pack to packetize your data
        # into a usable payload
        #buffer = struct.pack("<f", payload)
        #print(payload)
        buffer = struct.pack("p", payload)
        #print(buffer)
        # "<f" means a single little endian (4 byte) float value.
        start_timer = time.monotonic_ns()  # start timer
        result = nrf.send(payload)
        end_timer = time.monotonic_ns()  # end timer
        if not result:
            print("send() failed or timed out")
        #else:
        #    print(
        #        "Transmission successful! Time to Transmit: "
        #        "{} us. Sent: {}".format(
        #            (end_timer - start_timer) / 1000, payload
        #        )
        #    )
        #payload[0] += 0.01
        #time.sleep(1)
        count -= 1


def slave(timeout=60):
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
            # expecting a little endian float, thus the format string "<f"
            # buffer[:4] truncates padded 0s if dynamic payloads are disabled
            payload[0] = struct.unpack("<f", buffer[:4])[0]
            # print details about the received packet
            print(
                "Received {} bytes on pipe {}: {}".format(
                    payload_size, pipe_number, payload[0]
                )
            )
            start = time.monotonic()

    # recommended behavior is to keep in TX mode while idle
    nrf.listen = False  # put the nRF24L01 is in TX mode
t = time.time()
master()
print('time to finish: '+str(time.time()-t))
