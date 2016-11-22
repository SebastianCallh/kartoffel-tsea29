from time import sleep

from bus import GYRO_ADDR
from eventbus import EventBus
from utils import twos_comp


GYRO_LOWER_LIMIT = 10

class Gyro:
    
    
    @staticmethod
    def initialize():
        #Set the PD flag to 1 to go from power-down mode to normal mode
        EventBus.bus.bus.write_byte_data(GYRO_ADDR, 0x20, 0x0F)
        EventBus.bus.bus.write_byte_data(GYRO_ADDR, 0x23, 0x30)
         
        
    @staticmethod
    def read_data():
        try:
            hi = EventBus.bus.bus.read_byte_data(GYRO_ADDR, 0x2d)
            lo = EventBus.bus.bus.read_byte_data(GYRO_ADDR, 0x2c)
            data = (hi << 8) | lo
            
            #Divided by gyro sensitivity 18/256 for 2000 dps
            two_comp_data = 18 * twos_comp(data, 16) / 256
                    
            #To prevent garbage values while standing still
            if abs(two_comp_data) <= GYRO_LOWER_LIMIT:
                return 0
                
            return two_comp_data
            
        except:
            return -1