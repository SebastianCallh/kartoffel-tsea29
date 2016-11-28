from eventbus import EventBus
from protocol import LASER_ADDR
from time import sleep


class Laser:
    def __init__(self):
        self.data = 0

    def get_data(self):
        return self.data

    def read_data(self):
        try:
            hi = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x0f)
            lo = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x10)
            data = (hi << 8) | lo

            if hi & 0x80 == 128 or (lo == 1 and hi == 0):
                self.data = -1
            else:
                self.data = data * 10
        except:
            self.data = -1

    @staticmethod
    def initialize():
        # Was bus.write_byte_data, but that method was renamed/removed
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x00)  # Resets FPGA registers
        sleep(1)
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x11, 0xff)  # sets laser to read forever
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x04)  # sets laser to start reading
