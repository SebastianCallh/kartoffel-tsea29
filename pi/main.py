"""
Main program code - where all the magic happens
"""

from datetime import datetime, timedelta

from navigator import Navigator
from driver import Driver
from laser import Laser
from gyro import Gyro

from eventbus import EventBus
from position import Position

from protocol import *
from safety import Safety

import bt_server_cmds
import outbound

laser = Laser()
gyro = Gyro()
driver = Driver(gyro, laser)
navigator = Navigator(driver, laser)
position = Position()

# Update frequency
last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False

current_ir_left_mm = 0
current_ir_right_mm = 0


def sensor_data_requested():
    outbound.bt_return_sensor_data(str(current_ir_left_mm) + ", "+str(current_ir_right_mm))


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(BT_REQUEST_SENSOR_DATA, sensor_data_requested)
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, sensor_data_received)
    EventBus.subscribe(REQUEST_PI_IP, ip_requested)
    EventBus.subscribe(TEST_HI, return_hi)
    Laser.initialize()
    Gyro.initialize()


def sensor_data_received(ir_left_mm, ir_right_mm):
    global busy, navigator,current_ir_left_mm,current_ir_right_mm
    current_ir_left_mm = ir_left_mm
    current_ir_right_mm = ir_right_mm
    busy = False
    navigator.sensor_data_received(ir_left_mm, ir_right_mm)


def ip_requested():
    ip = bt_server_cmds.get_pi_ip()
    # Put IP on the bus
    outbound.return_ip(ip)


def return_hi():
    outbound.test_ho()


def request_data():
    global busy, last_request, request_period
    if not busy and datetime.now() - last_request > request_period:
        busy = True
        last_request = datetime.now()

        # TODO: Uncomment below line when reading from laser
        # laser_distance = Laser.read_data()

        outbound.request_sensor_data()


def main():
    global busy, last_request
    setup()

    while True:
        EventBus.receive()
        request_data()
        position.update()
        navigator.navigate()


Safety.run_safely(main)
