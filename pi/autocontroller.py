import datetime
from math import floor

time_last_regulation = datetime.datetime.now()
use_derivate = True
old_error = 0
integral = 0


class AutoController:
    def auto_control(self, ir_left_mm, ir_right_mm, reg_side):
        global use_derivate, time_last_regulation, old_error, integral

        DESIRED_DISTANCE = 120  # Desired distance to wall
        STANDARD_SPEED = 25


        Kp = float(0.3)
        Kd = float(0.2)

        time_now = datetime.datetime.now()
        sensor_data_front = ir_right_mm
        sensor_data_back = ir_left_mm
        dist_diff = (sensor_data_front - sensor_data_back) / 10



        regulation_error = DESIRED_DISTANCE - sensor_data_front
        delta_t = (time_now - time_last_regulation).microseconds / 1000

        regulation = floor((Kp * regulation_error) + dist_diff )#(Kd / delta_t * (regulation_error - old_error)))

        old_error = regulation_error


        if (regulation > -10):
            speed_close_wall = STANDARD_SPEED + regulation
        else:
            speed_close_wall = 10

        if (regulation < 10):
            speed_far_wall = STANDARD_SPEED - regulation
        else:
            speed_far_wall = 10

        time_last_regulation = time_now
        
        return int(speed_close_wall), int(speed_far_wall), regulation
