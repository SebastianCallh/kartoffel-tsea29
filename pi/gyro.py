from bus import GYRO_ADDR
from eventbus import EventBus
from time import sleep

class Gyro:
    
    
    @staticmethod
    def initialize():
        #Set the PD flag to 1 to go from power-down mode to normal mode
        EventBus.bus.bus.write_byte_data(GYRO_ADDR, 0x20, 0x0F)
        
        
    @staticmethod
    def read_data():
        try:
            hi = EventBus.bus.bus.read_byte_data(GYRO_ADDR, 0x2d)
            lo = EventBus.bus.bus.read_byte_data(GYRO_ADDR, 0x2c)
            data = (hi << 8) | lo
            return data
        except:
            return -1