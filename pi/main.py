"""
Main program code - where all the magic happens
"""

from datetime import datetime, timedelta

from navigator import Navigator
from driver import Driver
from laser import Laser
from gyro import Gyro
from ir import IR
from bt_data_handler import Data_handler

from eventbus import EventBus
from position import Position

from protocol import *
from safety import Safety

ir = IR()
laser = Laser()
gyro = Gyro()
driver = Driver(gyro, laser)
navigator = Navigator(ir, driver, laser)
position = Position(laser)
data_handler = Data_handler(ir, laser, gyro, driver, position)


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(BT_REQUEST_SENSOR_DATA, data_handler.send_sensor_data)
    EventBus.subscribe(BT_REQUEST_SERVO_DATA, data_handler.send_servo_data)
    EventBus.subscribe(BT_REQUEST_MAP_DATA, data_handler.send_map_data)
    EventBus.subscribe(BT_REQUEST_PI_IP, data_handler.send_ip)
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, ir.sensor_data_received)
    Laser.initialize()
    Gyro.initialize()
    Data_handler.initialize()


def main():
    setup()

    while True:
        laser.read_data()
        gyro.read_data()
        ir.request_data()

        EventBus.receive()
        position.update()
        navigator.navigate()


Safety.run_safely(main)
