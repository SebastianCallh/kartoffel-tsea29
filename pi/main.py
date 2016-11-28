"""
Main program code - where all the magic happens
"""

from datetime import datetime, timedelta

from navigator import Navigator
from driver import Driver
from laser import Laser
from gyro import Gyro
from ir import IR
from bluetooth import Bluetooth

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
ir = IR(navigator)
position = Position(laser)
bluetooth = Bluetooth(ir, laser, gyro, driver, position)


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(BT_REQUEST_SENSOR_DATA, bluetooth.send_sensor_data())
    EventBus.subscribe(BT_REQUEST_SERVO_DATA, bluetooth.send_servo_data())
    EventBus.subscribe(BT_REQUEST_MAP_DATA, bluetooth.send_map_data())
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, ir.sensor_data_received)
    EventBus.subscribe(REQUEST_PI_IP, ip_requested)
    Laser.initialize()
    Gyro.initialize()


def ip_requested():
    ip = bt_server_cmds.get_pi_ip()
    # Put IP on the bus
    outbound.return_ip(ip)


def main():
    setup()

    while True:
        EventBus.receive()
        ir.request_data()
        position.update()
        navigator.navigate()


Safety.run_safely(main)
