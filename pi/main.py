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
navigator = Navigator(Navigator.MANUAL, ir, driver, laser)
position = Position(laser)
communicator = Communicator(ir, laser, gyro, driver, position)


def setup():
    Safety.setup_terminal_abort() 
    EventBus.subscribe(BT_REQUEST_SENSOR_DATA, communicator.send_sensor_data)
    EventBus.subscribe(BT_REQUEST_SERVO_DATA, communicator.send_servo_data)
    EventBus.subscribe(BT_REQUEST_MAP_DATA, communicator.send_map_data)
    EventBus.subscribe(BT_DRIVE_FORWARD, communicator.drive_forward)
    EventBus.subscribe(BT_DRIVE_BACK, communicator.drive_backward)
    EventBus.subscribe(BT_TURN_RIGHT, communicator.turn_right)
    EventBus.subscribe(BT_TURN_LEFT, communicator.turn_left)
    EventBus.subscribe(BT_DRIVE_FORWARD_RIGHT, communicator.drive_forward_right)
    EventBus.subscribe(BT_DRIVE_FORWARD_LEFT, communicator.drive_forward_left)
    EventBus.subscribe(BT_AUTONOMOUS_MODE, navigator.set_mode(Navigator.AUTONOMOUS))
    EventBus.subscribe(BT_MANUAL_MODE, navigator.set_mode(Navigator.MANUAL))
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
