from datetime import datetime, timedelta
from outbound import set_motor_speed
	
###### METHODS FOR CONTROLLING THE WHEELS #######	


class Driver:

	TURN_SPEED = 45
	TURN_TIME = 900

	drive_stop_time = 0

	def driving(self):
		if drive_stop_time <= datetime.now():
			set_motor_speed(bus, 0, 0)
			return False
		return True

	def drive(self, left_speed, right_speed, duration):
		drive_stop_time = datetime.now() + timedelta(milliseconds=duration)
		set_motor_speed(bus, left_speed, right_speed)
			
	def turn_left(self):
		drive(-TURN_SPEED, TURN_SPEED, TURN_TIME)

	def turn_right(self):
		drive(TURN_SPEED, -TURN_SPEED, TURN_TIME)
		
	def prepare_for_turn(self):
		drive(40, 40, 600)
