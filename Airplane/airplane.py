from bin.nrf24.nrf import NRF
import time
import videoCapture

"""NRF24l01 init"""
## NRF() class is a wrapper of the circuit python RF24 
commA = NRF()

"""Test for client receive"""
def test_comms(count=0, test_packets=10, n=0):
    while count < test_packets:
        n += commA.send_test()
        count += 1
        time.sleep(0.5)
    return count, n
print('sent: {} awk: {} pingavg: {}'.format(*test_comms(), commA.pop_average_ping()))

"""Test video"""
VS = videoCapture.VideoStream()
payload = VS.get_frame()
commA.transmitBytes(payload)
