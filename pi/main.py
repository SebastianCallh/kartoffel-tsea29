"""
Main program code - where all the magic happens
"""

import signal
import sys
import traceback
from math import floor
from datetime import datetime, timedelta

from laser import Laser
from eventbus import EventBus
from outbound import request_sensor_data, \
    set_motor_speed, set_right_motor_speed, test_ho, return_ip

# Update frequency
from protocol import CMD_RETURN_SENSOR_DATA, REQUEST_PI_IP, TEST_HI
from safety import Safety

# For bluetooth
import protocol
import bt_server_cmds
import bt_task_handler

last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False

DESIRED_DIST = 100  # Desired distance to wall

old_e = 0
old_t = datetime.now()
Kp = 0.1


def sensor_data_received(ir_left_mm, ir_right_mm):
    global busy
    busy = False

    # print('ir_left_mm: ' + str(ir_left_mm))
    print('ir_right_mm: ' + str(ir_right_mm))

def ip_requested():
    ip = bt_server_cmds.get_pi_ip()
    # Put IP on the bus
    return_ip(ip)

def return_hi():
    test_ho()

def setup():
    Safety.setup_terminal_abort()
    #EventBus.subscribe(CMD_RETURN_SENSOR_DATA, sensor_data_received)
    EventBus.subscribe(REQUEST_PI_IP, ip_requested)
    EventBus.subscribe(TEST_HI, return_hi)
    Laser.initialize()


def main():
    global busy, last_request
    setup()

    while True:
        EventBus.receive()

        # rcv    check cmd    exc cmd   (send bt)

        """if not busy and datetime.now() - last_request > request_period:
            busy = True
            last_request = datetime.now()

            laser_distance = Laser.read_data()

            request_sensor_data()"""


Safety.run_safely(main)
