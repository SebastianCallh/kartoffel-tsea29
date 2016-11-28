import datetime
from math import floor

time_last_regulation = datetime.datetime.now()
use_derivate = True
old_error = 0
integral = 0
last_diff = 0


class AutoController:
    def auto_control(self, ir_right_mm, ir_right_back_mm, reg_side):
        global use_derivate, time_last_regulation, old_error, integral, last_diff

        DESIRED_DISTANCE = 120  # Desired distance to wall
        STANDARD_SPEED = 25
        MAX_REGULATION = 30

        Kp = float(0.2)
        Ka = float(0.3)

        time_now = datetime.datetime.now()
        sensor_data_front = ir_right_mm
        sensor_data_back = ir_right_back_mm
        dist_diff = (sensor_data_back - sensor_data_front)

        regulation_error = DESIRED_DISTANCE - sensor_data_front + abs(dist_diff / 10)

        if (sensor_data_front == -1 and sensor_data_back == -1):
            dist_diff = 0
            regulation_error = 0

        if (sensor_data_front != -1 and sensor_data_back == -1):
            regulation_error = DESIRED_DISTANCE - sensor_data_front

        regulation = floor((Kp * regulation_error) + Ka * dist_diff)

        old_error = regulation_error
        last_diff = dist_diff

        if (regulation > MAX_REGULATION):
            regulation = MAX_REGULATION
        elif (regulation < -MAX_REGULATION):
            regulation = -MAX_REGULATION

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
