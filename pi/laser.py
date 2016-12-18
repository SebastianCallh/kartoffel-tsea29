from eventbus import EventBus
from protocol import LASER_ADDR
from time import sleep

DEBUG_LASER = True

class Laser:
    DELTA_LIMIT = 100
    def __init__(self):
        self.data = 0
        self.last_data = 0
        self.last_last_data = 0
        
        if DEBUG_LASER:
            self.debug_file = open('laser_measurements.dat', 'w')
        else:
            self.debug_file = None

    def get_data(self):
        if  abs(self.data - self.last_data) < Laser.DELTA_LIMIT and \
            abs(self.data - self.last_last_data) < Laser.DELTA_LIMIT:
            return self.data
        else:
            return -1
            
    def read_data(self):
        try:
            hi = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x0f)
            lo = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x10)
            data = (hi << 8) | lo

            self.last_last_data = self.last_data
            self.last_data = self.data
            
            if hi & 0x80 == 128 or (lo == 1 and hi == 0):
                self.data = -1
            else:
                if data < self.data or self.data == 0:
                    new_data = data * 10
                    self.last_last_data = self.last_date
                    self.last_data = self.data
                    self.data = new_data
        except:
            self.data = -1

        if self.debug_file is not None:
            self.debug_file.write(str(self.get_data()) + '\n')
            self.debug_file.flush()

    def reset(self):
        self.data = 0
        self.last_data = 0
        self.last_last_data = 0
        
    @staticmethod
    def initialize():
        # Was bus.write_byte_data, but that method was renamed/removed
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x00)  # Resets FPGA registers
        sleep(1)
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x11, 0xff)  # sets laser to read forever
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x04)  # sets laser to start reading
