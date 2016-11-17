"""
Main program code - where all the magic happens
"""

from datetime import datetime, timedelta

from navigator import Navigator
from driver import Driver
from laser import Laser

from eventbus import EventBus
from outbound import request_sensor_data
from position import Position

from protocol import CMD_RETURN_SENSOR_DATA
from safety import Safety

laser = Laser()
driver = Driver()
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


def sensor_data_received(ir_left_mm, ir_right_mm):
    global busy, navigator
    busy = False
    navigator.sensor_data_received(ir_left_mm, ir_right_mm)


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
        navigator.navigate()


Safety.run_safely(main)
