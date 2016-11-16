from eventbus import EventBus
from protocol import LASER_ADDR
import time

class Laser:
    @staticmethod
    def initialize():
        #Was bus.write_byte_data, but that method was renamed/removed
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x00) #Resets FPGA registers
        time.sleep(1)
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x11, 0xff) #sets laser to read forever
        EventBus.bus.bus.write_byte_data(LASER_ADDR, 0x00, 0x04) #sets laser to start reading
        
    @staticmethod
    def read_data():
        try:
            hi = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x0f)
            lo = EventBus.bus.bus.read_byte_data(LASER_ADDR, 0x10)
            data = (hi << 8) | lo
            if hi & 0x80 == 128:
                return -1
            else:
                return data * 10
        except:
            return -1
