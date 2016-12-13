import datetime
from math import floor

time_last_regulation = datetime.datetime.now()
use_derivate = True
old_error = 0
integral = 0
last_diff = 0
last_valid_diffs = []
last_valid_diff = 0

QUEUE_SIZE = 15

class AutoController:
    DESIRED_DISTANCE = 120  # Desired distance to wall
    STANDARD_SPEED = 40
    MAX_REGULATION = 30

    def auto_control(self, ir_right_mm, ir_right_back_mm, reg_side):
        global use_derivate, time_last_regulation, old_error, integral, last_diff, last_valid_diff, last_valid_diffs

        Kp = float(0.2)
        Ka = float(0.3)

        time_now = datetime.datetime.now()
        sensor_data_front = ir_right_mm
        sensor_data_back = ir_right_back_mm
        dist_diff = (sensor_data_back - sensor_data_front)

        regulation_error = self.DESIRED_DISTANCE - sensor_data_front + abs(dist_diff / 10)


        if (sensor_data_front == -1 or sensor_data_back == -1):
            dist_diff = 0
            regulation_error = 0
        else:
            if len(last_valid_diffs) >= QUEUE_SIZE:
                last_valid_diffs = last_valid_diffs[1:QUEUE_SIZE] + [dist_diff]
            else:
                last_valid_diffs = last_valid_diffs + [dist_diff]
                
            last_valid_diff = last_valid_diffs[0]

        regulation = floor((Kp * regulation_error) + Ka * dist_diff)

        old_error = regulation_error
        last_diff = dist_diff

        if (regulation > self.MAX_REGULATION):
            regulation = self.MAX_REGULATION
        elif (regulation < -self.MAX_REGULATION):
            regulation = -self.MAX_REGULATION

        if (regulation > -10):
            speed_close_wall = self.get_speed(ir_right_mm, ir_right_back_mm) + regulation
        else:
            speed_close_wall = 10

        if (regulation < 10):
            speed_far_wall = self.get_speed(ir_right_mm, ir_right_back_mm) - regulation
        else:
            speed_far_wall = 10

        time_last_regulation = time_now
        
        return int(speed_close_wall), int(speed_far_wall), regulation

    def get_speed(self, ir_right_mm, ir_right_back_mm):
        if ir_right_mm == -1 and ir_right_back_mm != -1:
            return self.STANDARD_SPEED / 2
        else:
            return self.STANDARD_SPEED
