from time import sleep

from bus import ACCEL_ADDR
from eventbus import EventBus
from utils import twos_comp


class Accel:
    @staticmethod
    def initialize():
        #Set the PD flag to 1 to go from power-down mode to normal mode
        EventBus.bus.bus.write_byte_data(ACCEL_ADDR, 0x20, 0x51)
        EventBus.bus.bus.write_byte_data(ACCEL_ADDR, 0x23, 0x00)

    @staticmethod
    def read_data():
        try:
            x_hi = EventBus.bus.bus.read_byte_data(ACCEL_ADDR, 0x29)
            x_lo = EventBus.bus.bus.read_byte_data(ACCEL_ADDR, 0x28)
            x_data = ((x_hi << 8) | x_lo)

            y_hi = EventBus.bus.bus.read_byte_data(ACCEL_ADDR, 0x2b)
            y_lo = EventBus.bus.bus.read_byte_data(ACCEL_ADDR, 0x2a)
            y_data = ((y_hi << 8) | y_lo)

            x_two_comp_data = twos_comp(x_data, 16)
            y_two_comp_data = twos_comp(y_data, 16)

            #Multiplied by earths gravity and 0.001
            x_two_comp_data = x_two_comp_data * 0.001 * 9.82
            y_two_comp_data = y_two_comp_data * 0.001 * 9.82
            # To prevent garbage values while standing still

            return x_two_comp_data, y_two_comp_data

        except:
            return -1
