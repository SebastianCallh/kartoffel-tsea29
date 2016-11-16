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
    set_motor_speed, set_right_motor_speed


# Update frequency
from protocol import CMD_RETURN_SENSOR_DATA
from saftey import Safety

last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False

DESIRED_DIST = 100 # Desired distance to wall

old_e = 0
old_t = datetime.now()
Kp = 0.1


def sensor_data_received(ir_left_mm, ir_right_mm):
    global busy
    busy = False

    #print('ir_left_mm: ' + str(ir_left_mm))
    print('ir_right_mm: ' + str(ir_right_mm))

    u = auto_ctrl(ir_right_mm)

    print('u: ' + str(u))

    

# Reglerteknik
def auto_ctrl(ir_right_mm):
    global curr_speed_r, old_t
    t = datetime.now()

    if (t - old_t >= 500):
        if (ir_right_mm == -1):
            u = 0
            print("no reglering")
            set_motor_speed(curr_speed_l)
        else:
            e = DESIRED_DIST - ir_right_mm # reglerfelet

            # **** P-reglering *********
            u = floor(Kp * e) # styrsignal

            # ****** PD-reglering *********
            """global old_e
            u = Kp * e + Kd / (t - old_t) * (e - old_e)
            old_e = e
            """
            curr_speed_r = curr_speed_r + u
            set_right_motor_speed(curr_speed_r)
        old_t = t

    return u


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, sensor_data_received)
    Laser.initialize()


def main():
    global busy, last_request

    setup()

    while True:
        EventBus.receive()
    
	#read_bt()
	#rcv    check cmd    exc cmd   (send bt) 

        if not busy and datetime.now() - last_request > request_period:
            busy = True
            last_request = datetime.now()

            laser_distance = Laser.read_data()

            request_sensor_data()

curr_speed_l = 20
curr_speed_r = 20
set_motor_speed(curr_speed_r)

Safety.run_safely(main)
