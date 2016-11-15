import signal
import sys
import traceback
import datetime
from datetime import timedelta

from bus import Bus
from navigator import Navigator
from driver import Driver

from messages import read_messages, subscribe_to_cmd
from outbound import request_sensor_data, CMD_RETURN_SENSOR_DATA, \
set_motor_speed, set_right_motor_speed, set_left_motor_speed

bus = Bus()
driver = Driver(bus)
navigator = Navigator(driver)

# Update frequency
last_request = datetime.datetime.now()
request_period = timedelta(milliseconds=1)
busy = False

def sensor_data_received(ir_left_mm, ir_right_mm):
	global busy, navigator
	busy = False
	print('ir right': ir_right_mm)
	navigator.sensor_data_received(ir_left_mm, ir_right_mm)

def handle_abort(signum, frame):
	# Stop motors to avoid robot running amok
	set_motor_speed(bus, 0)

	sys.exit(0)

def handle_bus(bus):
	global busy, last_request, request_period
	if not busy and datetime.datetime.now() - last_request > request_period:
		busy = True
		last_request = datetime.datetime.now()

	request_sensor_data(bus)

# Setup
signal.signal(signal.SIGINT, handle_abort)
subscribe_to_cmd(CMD_RETURN_SENSOR_DATA, sensor_data_received)

try:
	while True:
		read_messages(bus)
		handle_bus(bus)
		navigator.navigate()


except:
	traceback.print_exc()
	set_motor_speed(bus, 0)