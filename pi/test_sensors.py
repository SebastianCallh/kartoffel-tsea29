"""
Main program code - where all the magic happens
"""
from math import floor
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

# Update frequency
last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False

l_r = datetime.now()
r_p = timedelta(milliseconds=250)


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, sensor_data_received)
    Laser.initialize()
    Gyro.initialize()


def sensor_data_received(ir_left_mm, ir_right_mm, ir_right_back_mm, ir_left_back_mm):
    global busy, navigator
    busy = False

    if datetime.now() - l_r > r_p:
        diff = ir_right_back_mm - ir_right_mm
        print ("Diff: " + str())
        print ("Wall dist: " + str(floor(120 - (ir_right_mm) + abs(diff / 10))))
    #print("LF: " + str(ir_left_mm))
    #print("RF: " + str(ir_right_mm))
    #print("RBack: " + str(ir_right_back_mm))
    #print("LBack: " + str(ir_left_back_mm))


def request_data():
    global busy, last_request, request_period
    if not busy and datetime.now() - last_request > request_period:
        busy = True
        last_request = datetime.now()

        # TODO: Uncomment below line when reading from laser
        laser_distance = Laser.read_data()
        #print("Laser distance: " + str(laser_distance))
        request_sensor_data()


def main():
    global busy, last_request

    setup()

    while True:
        EventBus.receive()
        request_data()

Safety.run_safely(main)
