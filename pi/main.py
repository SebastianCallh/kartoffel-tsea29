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


def sensor_data_received(ir_left_mm, ir_right_mm):
    global busy
    busy = False

    print('ir_left_mm: ' + str(ir_left_mm))
    print('ir_right_mm: ' + str(ir_right_mm))


def handle_abort(signum, frame):
    # Stop motors to avoid robot running amok
    set_motor_speed(bus, 0)

    sys.exit(0)

# Setup
subscribe_to_cmd(CMD_RETURN_SENSOR_DATA, sensor_data_received)
signal.signal(signal.SIGINT, handle_abort)

while True:
    read_messages(bus)

    if not busy and datetime.now() - last_request > request_period:
        busy = True
        last_request = datetime.now()

        request_sensor_data(bus)
