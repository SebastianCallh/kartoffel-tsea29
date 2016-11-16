from datetime import datetime, timedelta
from outbound import set_motor_speed
	
###### METHODS FOR CONTROLLING THE WHEELS #######	

TURN_SPEED = 45
TURN_TIME = 900

class Driver:

    def __init__(self):
        self.drive_stop_time = 0
        self.tasks = []

    def driving(self):
        print('time left driving: ' + str(self.drive_stop_time - datetime.now()))
        if self.drive_stop_time <= datetime.now():
            #If tasks are complete, the robot is no longer driving
            if not self.tasks:
                set_motor_speed(0, 0, 500)
                return False
            
            self.tasks.pop()()
        return True

    def drive(self, left_speed, right_speed, duration):
        self.drive_stop_time = datetime.now() + timedelta(milliseconds=duration)
        set_motor_speed(left_speed, right_speed)
    
    def out_right_turn(self):
        self.tasks = [nudge_forward, turn_right, nudge_forward]

    def outer_left_turn(self):
        self.tasks = [nudge_forward, turn_left, nudge_forward]

    def inner_left_turn(self):
        self.tasks = [turn_left]

    def inner_right_turn(self):
        self.tasks = [turn_right]

    #Not intended for public use

    def _turn_left(self):
        self.drive(-TURN_SPEED, TURN_SPEED, TURN_TIME)

    def _turn_right(self):
        self.drive(TURN_SPEED, -TURN_SPEED, TURN_TIME)
   
    def _nudge_forward(self):
        self.drive(40, 40, 400)