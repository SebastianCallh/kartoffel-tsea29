from bus import LASER_ADDR
from eventbus import EventBus


class Laser:
    @staticmethod
    def initialize():
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x00) #Resets FPGA registers
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x11, 0xff) #sets laser to read forever
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x04) #sets laser to start reading

    @staticmethod
    def read_data():
        try:
            hi = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x0f)
            lo = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x10)
            data = (hi << 8) | lo
            return data * 10
        except:
            return -1
