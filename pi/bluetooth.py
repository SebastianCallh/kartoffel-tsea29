import outbound

from utils import get_ip

class Bluetooth:
    def __init__(self, ir, laser, gyro, driver, position):
        self.ir = ir
        self.laser = laser
        self.gyro = gyro
        self.driver = driver
        self.position = position

    '''
    Sends the sensor data as a string of integers on the format
    "ir_left, ir_left_back, ir_right, ir_right_back, laser, gyro"
    '''
    def send_sensor_data(self):
        outbound.bt_return_sensor_data(self.ir.get_ir_left() + ', ' +
                                       self.ir.get_ir_left_back() + ', ' +
                                       self.ir.get_ir_right() + ', ' +
                                       self.ir.get_ir_right_back() + ', ' +
                                       self.laser.get_data() + ', ' +
                                       self.gyro.get_data())

    '''
    Sends the sensor data as a string of integers on the format
    "left_speed, right_speed"
    '''
    def send_servo_data(self):
        outbound.bt_return_servo_data(self.driver.get_left_speed() + ', ' +
                                      self.driver.get_right_speed())

    '''
    Sends the map data as a list with tuples of integers corresponding to corner coordinates on the format
    "[(X1, Y1), (X2, Y2), ... , (Xn, Yn)]"
    '''
    def send_map_data(self):
        outbound.bt_return_map_data(str(self.position.get_map_data()))

    def send_ip(self):
        outbound.bt_return_ip(get_ip())