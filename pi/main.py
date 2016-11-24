"""
Main program code - where all the magic happens
"""

from datetime import datetime, timedelta

from navigator import Navigator
from driver import Driver
from laser import Laser
from gyro import Gyro

from eventbus import EventBus
from outbound import request_sensor_data
from position import Position

from protocol import CMD_RETURN_SENSOR_DATA
from safety import Safety

laser = Laser()
gyro = Gyro()
driver = Driver(gyro, laser)
navigator = Navigator(driver, laser)
position = Position()

# Update frequency
last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, sensor_data_received)
    Laser.initialize()
    Gyro.initialize()


def sensor_data_received(ir_left_mm, ir_right_mm, ir_right_back_mm, ir_left_back_mm):
    global busy, navigator
    busy = False
    print("LF: " + str(ir_left_mm))
    print("RF: " + str(ir_right_mm))
    print("RBack: " + str(ir_right_back_mm))
    print("LBack: " + str(ir_left_back_mm))
    navigator.sensor_data_received(ir_left_mm, ir_right_mm, ir_right_back_mm, ir_left_back_mm)


def request_data():
    global busy, last_request, request_period
    if not busy and datetime.now() - last_request > request_period:
        busy = True
        last_request = datetime.now()

        # TODO: Uncomment below line when reading from laser
        # laser_distance = Laser.read_data()

        request_sensor_data()


def main():
    global busy, last_request

    setup()

    while True:
        EventBus.receive()
        request_data()
        #position.update()
        #navigator.navigate()


Safety.run_safely(main)
