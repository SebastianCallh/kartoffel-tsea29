def init_laser_data(bus):
    bus.write_byte_data(0x62, 0x11, 0xff) #sets laser to read forever
    bus.write_byte_data(0x62, 0x00, 0x04) #sets laser to start reading

def read_laser_data(bus):
    try:
        hi = bus.read_byte_data(0x62, 0x14)
        lo = bus.read_byte_data(0x62, 0x15)
        data = (hi << 8) | lo
        return data
    except:
        return read_laser_data(bus)
