try:
    from rf24 import RF24
except:
    from nrf24.rf24 import RF24
import time
import struct
import board
import digitalio


class NRF(RF24):
    """My custom wrapper of the RF24 class V2.0.1"""

    def __init__(self,radioNum, ce=None, csn=None, pa=None, data_r=None, cha=None):
        if not ce: ce = digitalio.DigitalInOut(board.D22)
        if not csn: csn = digitalio.DigitalInOut(board.D8)
        spi = board.SPI()
        try:
            super().__init__(spi, csn, ce)
        except:
            '_RF24 init failed, check wiring'
        # Set the PA. high(0,-6,-12,-18)low
        if not pa: self.pa_level = -12
        # Set the data transmission rate. (2,1)2Mbps,1Mbps
        if not data_r: self.data_rate = 2
        # [0, 125],  [2.4, 2.525]GHz
        if not cha: self.channel = 125
        print(self.print_details())
        # addresses needs to be in a buffer protocol object (bytearray)
        address = [b"1Node", b"2Node"]
        radio_number = bool(radioNum)
        # set TX address of RX node into the TX pipe
        self.open_tx_pipe(address[radio_number])  # always uses pipe 0
        # set RX address of TX node into an RX pipe
        self.open_rx_pipe(1, address[not radio_number])  # using pipe 1
        self.transmit_times = []

    def print_average_ping(self):
        val = sum(self.transmit_times) / len(self.transmit_times)
        print(
            "Average Ping: "
            "{} us.".format(
                (val / 1000)
            )
        )

    def pop_average_ping(self):
        val = sum(self.transmit_times) / len(self.transmit_times)
        self.transmit_times.clear()
        return (val / 1000)

    def send_test(self, response=False):
        payload = b'testtesttesttesttesttesttesttest'
        print(len(payload))
        self.listen = False  # ensures the nRF24L01 is in TX mode
        start_timer = time.monotonic_ns()  # start timer
        result = self.send(payload)
        end_timer = time.monotonic_ns()  # end timer
        if not result:
            print("send() failed or timed out")
        else:
            response = True
            self.transmit_times.append(end_timer - start_timer)
            print(
                "Transmission successful! Time to Transmit: "
                "{} us. Sent: {}".format(
                    (end_timer - start_timer) / 1000, payload
                )
            )
        return response

    def transmitBytes(self, bytes, response=False):
        self.listen = False  # ensures the nRF24L01 is in TX mode
        result = self.send(b"Array")
        if not result:
            return response
        split_payload = [bytes[i:i + 32] for i in range(0, len(bytes), 32)]
        start_timer = time.monotonic_ns()  # start timer
        result = self.send(split_payload)
        end_timer = time.monotonic_ns()  # end timer
        if not result:
            print("send() failed or timed out")
        else:
            self.transmit_times.append(end_timer - start_timer)
            print(
                "Transmission successful! Time to Transmit: "
                "{} us. ".format((end_timer - start_timer) / 1000, ))
        result = self.send(b"ArrayFinish")
        if not result:
            return response
        response = True
        return response

    def request_telemetry(self):
        #print(self)
        data = {'speed': 10,
                'heading': 270,
                'pitch': 20,
                'roll': 20,
                'yaw': 10,
                'throttle': 5,
                'altitude': 100}
        # send request packet, wait for responce
        return data
