from datetime import datetime, timedelta
from outbound import set_motor_speed
	
###### METHODS FOR CONTROLLING THE WHEELS #######	

TURN_SPEED = 45
TURN_TIME = 900

class Driver:

	def __init__(self):
		self.drive_stop_time = 0
		
	def driving(self):
		print('time left driving: ' + str(self.drive_stop_time - datetime.now()))
		if self.drive_stop_time <= datetime.now():
			set_motor_speed(0, 0)
			return False
		return True

	def drive(self, left_speed, right_speed, duration):
		self.drive_stop_time = datetime.now() + timedelta(milliseconds=duration)
		set_motor_speed(left_speed, right_speed)
			
	def turn_left(self):
		self.drive(-TURN_SPEED, TURN_SPEED, TURN_TIME)

	def turn_right(self):
		self.drive(TURN_SPEED, -TURN_SPEED, TURN_TIME)
		
	def prepare_for_turn(self):
		self.drive(20, 20, 600)
