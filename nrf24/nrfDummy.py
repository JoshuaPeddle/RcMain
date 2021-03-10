

class NRF:
    """My custom wrapper of the RF24 class V2.0.1"""

    def __init__(self):

        print('nrf dummy init')


    def print_average_ping(self):
        print(100)

    def pop_average_ping(self):
        return 100

    def send_test(self, response=False):

        response = True

        return response

    def transmitBytes(self, bytes, response=False):
        response = True
        return response

    def request_telemetry(self):
        # print(self)
        data = {'speed': 10,
                'heading': 270,
                'pitch': 20,
                'roll': 20,
                'yaw': 10,
                'throttle': 5,
                'altitude': 100}
        # send request packet, wait for responce
        return data
