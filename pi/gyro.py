from time import sleep

from protocol import GYRO_ADDR
from eventbus import EventBus
from utils import twos_comp

GYRO_LOWER_LIMIT = 10


class Gyro:
    def __init__(self):
        self.data = 0


    def get_data(self):
        return self.data

    def read_data(self):
        try:
            hi = EventBus.bus.bus.read_byte_data(GYRO_ADDR, 0x2d)
            lo = EventBus.bus.bus.read_byte_data(GYRO_ADDR, 0x2c)
            data = (hi << 8) | lo

            # Divided by gyro sensitivity 18/256 for 2000 dps
            two_comp_data = 18 * twos_comp(data, 16) / 256

            # To prevent garbage values while standing still
            if abs(two_comp_data) <= GYRO_LOWER_LIMIT:
                self.data = 0

            self.data = two_comp_data

        except:
            self.data = -1

    @staticmethod
    def initialize():
        # Set the PD flag to 1 to go from power-down mode to normal mode
        EventBus.bus.bus.write_byte_data(GYRO_ADDR, 0x20, 0x0F)
        EventBus.bus.bus.write_byte_data(GYRO_ADDR, 0x23, 0x30)

