from bus import LASER_ADDR
from eventbus import EventBus


class Laser:
    @staticmethod
    def initialize():
		#Was bus.write_byte_data, but that method was renamed/removed
        EventBus.bus._write_byte_data(LASER_ADDR, 0x11, 0xff) #sets laser to read forever
        EventBus.bus._write_byte_data(LASER_ADDR, 0x00, 0x04) #sets laser to start reading

    @staticmethod
    def read_data():
        try:
            hi = EventBus.bus._read_packet_data(LASER_ADDR, 0x0f)
            lo = EventBus.bus._read_packet_data(LASER_ADDR, 0x10)
            data = (hi << 8) | lo
            return data * 10
        except:
            return -1
