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


# Reglerteknik
"""def auto_ctrl(ir_right_mm):
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

global old_e
u = Kp * e + Kd / (t - old_t) * (e - old_e)
old_e = e

curr_speed_r = curr_speed_r + u
set_right_motor_speed(curr_speed_r)
old_t = t

return u"""


def setup():
    Safety.setup_terminal_abort()
    EventBus.subscribe(CMD_RETURN_SENSOR_DATA, sensor_data_received)
    # Laser.initialize()


def main():
    global busy, last_request
    setup()
    while True:
        EventBus.receive()

        # read_bt()
        bt_task = bt_task_handler.pop_incoming()
        # print("type of task =", type(bt_task))
        # print("task =", bt_task)
        if bt_task == None:
            # print("main: bt_task == None")
            pass
        elif int(bt_task.cmd_id) == protocol.REQUEST_PI_IP:
            print("main: bt_task.cmd_id = ", bt_task.cmd_id)
            ip = bt_server_cmds.get_pi_ip()
            bt_task_handler.post_outgoing(bt_task_handler.BT_task(protocol.SEND_PI_IP, ip))
            break

        # rcv    check cmd    exc cmd   (send bt)

        """if not busy and datetime.now() - last_request > request_period:
            busy = True
            last_request = datetime.now()

            laser_distance = Laser.read_data()

            request_sensor_data()"""


Safety.run_safely(main)
