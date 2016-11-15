import datetime

from math import floor

time_last_regulation = datetime.datetime.now()
use_derivate = True
old_error = 0

Kp = float(0.6)
Kd = float(2)

STANDARD_SPEED = 40
SLOW_SPEED = 20

class AutoController:

	def auto_control(self, ir_left_mm, ir_right_mm, reg_side):
		global use_derivate, time_last_regulation, old_error
		
		DESIRED_DISTANCE = 120 # Desired distance to wall
		
		time_now = datetime.datetime.now()

		if (ir_left_mm == -1 and ir_right_mm == -1): # Don't regulate
			regulation = 0
			print("u = 0, no reglering")
			set_motor_speed(bus, SLOW_SPEED)
			time_last_regulation = time_now
			use_derivate = False
			return
		elif (ir_left_mm != -1 and ir_right_mm != -1): # Regulate on right side
			reg_side = "right"
			sensor_data_dist = ir_right_mm
		elif (ir_left_mm == -1 and ir_right_mm != -1):
			reg_side = "right"
			sensor_data_dist = ir_right_mm
		elif (ir_left_mm != -1 and ir_right_mm == -1): # Only case for regulation on left
			reg_side = "left"
			sensor_data_dist = ir_left_mm
		else:
			reg_side = "right"
			sensor_data_dist = ir_right_mm

		regulation_error = DESIRED_DISTANCE - sensor_data_dist
		delta_t = (time_now - time_last_regulation).microseconds / 1000

		if(use_derivate == False):
			regulation = floor((Kp * regulation_error))
			use_derivate = True
			print("No derivate")
		else:
			regulation = floor((Kp * regulation_error) + (Kd / delta_t * (regulation_error - old_error)))

		old_error = regulation_error

		if (regulation > -10):
			speed_close_wall = STANDARD_SPEED + regulation
		else:
			speed_close_wall = 10
		print("speed_close_wall = " + str(speed_close_wall))

		if (regulation < 10):
			speed_far_wall = STANDARD_SPEED - regulation
		else:
			speed_far_wall = 10
		print("speed_far_wall = " + str(speed_far_wall))

		print("u: " + str(regulation))

		time_last_regulation = time_now
		
		return speed_close_wall, speed_far_wall
