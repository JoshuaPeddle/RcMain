class Airplane:

    def __init__(self):
        self.current_speed = 0  # read from gps
        self.heading = 0  # (0-359)  read from arduino
        self.pitch = 0  # (180,-180) read from arduino
        self.roll = 0  # (180,-180) read from arduino
        self.yaw = 0  # (180,-180)
        self.throttle = 0  # set from user control
        self.location = None  # Used when interfaced with GPS module
        self.start_location = None  # used when interfaced with gps module

    def build_airplane_config(self):
        supported_comms = {'x': 'NRF', 'y': 'LoRa'}
        gps_enabled = [True, False]
        print('Enter available comms: ')
        comms_selection = supported_comms[input('x: {x} \ny: {y} \nz: {x} & {y}\n'.format_map(supported_comms))]



A = Airplane()
A.build_airplane_config()