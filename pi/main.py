import signal
import sys
import traceback
from math import floor
from datetime import datetime, timedelta

from bus import Bus
from messages import read_messages, subscribe_to_cmd
from outbound import request_sensor_data, CMD_RETURN_SENSOR_DATA, \
    set_motor_speed, set_right_motor_speed, set_left_motor_speed

bus = Bus()

# Update frequency
last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False

DESIRED_DIST = 100 # Desired distance to wall

old_e = 0
old_t = datetime.now()
Kp = 0.1

TURN_SPEED = 20
TURN_TIME = 1000
turn_start_time = 0
curr_speed_l = 0
curr_speed_r = 0


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
            set_motor_speed(bus, curr_speed_l)
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
            set_right_motor_speed(bus, curr_speed_r)
        old_t = t

    return u



def handle_abort(signum, frame):
    # Stop motors to avoid robot running amok
    set_motor_speed(bus, 0)

    sys.exit(0)

def update_turn_state():
	if datetime.datetim.now() - turn_start_time >= datetime.timedelta(milliseconds=TURN_TIME)
		set_motor_speed(bus, 0, 0)
		
def turn_left():
	global turn_start_time = datetime.now()
	set_motor_speed(bus, -TURN_SPEED, TURN_SPEED)
	
def turn_right():
	global turn_start_time = datetime.now()
	set_motor_speed(bus, TURN_SPEED, -TURN_SPEED)


# Setup
#subscribe_to_cmd(CMD_RETURN_SENSOR_DATA, sensor_data_received)
signal.signal(signal.SIGINT, handle_abort)

turn_right()

try:
    while True:
		#read_messages(bus)

		update_turn_state()
		'''if not busy and datetime.now() - last_request > request_period:
            busy = True
            last_request = datetime.now()

            request_sensor_data(bus)
		'''
except:
    traceback.print_exc()
    set_motor_speed(bus, 0)
    