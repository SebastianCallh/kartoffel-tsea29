"""
Main program code - where all the magic happens
"""

from datetime import datetime, timedelta

from navigator import Navigator
from driver import Driver
from laser import Laser
from gyro import Gyro
from ir import IR
from communicator import Communicator

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
communicator = Communicator(ir, laser, gyro, driver, position)


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(BT_REQUEST_SENSOR_DATA, communicator.send_sensor_data)
    EventBus.subscribe(BT_REQUEST_SERVO_DATA, communicator.send_servo_data)
    EventBus.subscribe(BT_REQUEST_MAP_DATA, communicator.send_map_data)
    EventBus.subsribe(BT_DRIVE_FORWARD, Driver.drive_forward)
    EventBus.subsribe(BT_DRIVE_BACK, Driver.drive_backward)
    EventBus.subsribe(BT_TURN_RIGHT, Driver.turn_right)
    EventBus.subsribe(BT_TURN_LEFT, Driver.turn_left)
    EventBus.subscribe(REQUEST_PI_IP, communicator.send_ip)
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, ir.sensor_data_received)
    Laser.initialize()
    Gyro.initialize()


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
