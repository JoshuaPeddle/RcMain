import sys
sys.path.append('C:\\Users\\joshu\\OneDrive\\Desktop\\Github\\RcMain')
import threading
from LiveView import LiveView
import time

try:
    from nrf24.nrf import NRF

    commA = NRF()
    print('NRF running from supported hardware')
except:
    from nrf24.nrfDummy import NRF

    commA = NRF()
    print('NRF not found on this system, init dummyNRF')
"""NRF24l01 init"""
## NRF() class is a wrapper of the circuit python RF24


telemetry = commA.request_telemetry()
L = LiveView(telemetry)


class StringTest(threading.Thread):
    def __init__(self):
        super().__init__()
        self.val = 1

    def get_string(self):
        self.val += 1
        return str(self.val)

    def run(self):
        while not L.crashed:
            L.test_string = self.get_string()
            time.sleep(.01)


T = StringTest()
L.start()
T.start()
import random
import time
last_update = time.time()

while True:
    t =  time.time()
    # Update LiveView
    for event in L.game.event.get():
        if event.type == L.game.QUIT:
            L.crashed = True
    if last_update < t - .5:
        last_update = t
        #print('telemupdate')
        telem = commA.request_telemetry()
        telem['pitch'] = random.randint(-90,90)
        L.telemetry = telem
