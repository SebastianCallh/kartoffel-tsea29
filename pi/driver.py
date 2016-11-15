from datetime import datetime, timedelta
from outbound import set_motor_speed
	
###### METHODS FOR CONTROLLING THE WHEELS #######	

TURN_SPEED = 45
TURN_TIME = 900

class Driver:

	def __init__(self, bus):
		self.bus = bus
		self.drive_stop_time = 0
		
	def driving(self):
		print('time left driving: ' + str(self.drive_stop_time - datetime.now()))
		if self.drive_stop_time <= datetime.now():
			set_motor_speed(self.bus, 0, 0)
			return False
		return True

	def drive(self, left_speed, right_speed, duration):
		self.drive_stop_time = datetime.now() + timedelta(milliseconds=duration)
		set_motor_speed(self.bus, left_speed, right_speed)
			
	def turn_left(self):
		self.drive(-TURN_SPEED, TURN_SPEED, TURN_TIME)

	def turn_right(self):
		self.drive(TURN_SPEED, -TURN_SPEED, TURN_TIME)
		
	def prepare_for_turn(self):
		print('driver preparing for turn')
		self.drive(40, 40, 600)
