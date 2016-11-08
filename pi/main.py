import signal
import sys
from datetime import datetime, timedelta

from bus import Bus
from messages import read_messages, subscribe_to_cmd
from outbound import request_sensor_data, CMD_RETURN_SENSOR_DATA, \
    set_motor_speed

bus = Bus()

# Update frequency
last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False

DESIRED_DIST = 100 # Desired distance to wall

old_e = 0
old_t = datetime.now()
Kp = 1

curr_speed_l = 0
curr_speed_r = 0

def sensor_data_received(ir_left_mm, ir_right_mm):
    global busy
    busy = False
    t = datetime.now()

    print('ir_left_mm: ' + str(ir_left_mm))
    print('ir_right_mm: ' + str(ir_right_mm))
    

# Reglerteknik
def auto_ctrl(ir_right_mm):
    old_e, old_t
    e = des_dist - ir_right_mm # reglerfelet

    # **** P-reglering *********
    u = Kp * e # styrsignal

    # ****** PD-reglering *********
    """u = Kp * e + Kd / (t - old_t) * (e - old_e)
    old_e = e
    old_t = t"""

    curr_speed_r += u
    set_right_motor_speed(bus, curr_speed_r)



def handle_abort(signum, frame):
    # Stop motors to avoid robot running amok
    set_motor_speed(bus, 0)

    sys.exit(0)

# Setup
subscribe_to_cmd(CMD_RETURN_SENSOR_DATA, sensor_data_received)
signal.signal(signal.SIGINT, handle_abort)

curr_speed_l = 3
curr_speed_r = 3
set_motor_speed(bus, curr_speed_r)

while True:
    read_messages(bus)

    if not busy and datetime.now() - last_request > request_period:
        busy = True
        last_request = datetime.now()

        request_sensor_data(bus)
