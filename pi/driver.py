from datetime import datetime, timedelta
from outbound import set_motor_speed
	
###### METHODS FOR CONTROLLING THE WHEELS #######	
# Tasks should be reversed since we pop them from the list 

TURN_SPEED = 45
TURN_TIME = 900

class Driver:

    def __init__(self):
        self.drive_stop_time = 0
        self.tasks = []
        self.task = None
   
    def driving(self):
        if self.drive_stop_time <= datetime.now():
            #If tasks are complete, the robot is no longer driving
            if not self.tasks:
                self.stop()
                return False
            
            self.tasks.pop()()
            return True
        return True


    def drive(self, left_speed, right_speed, duration):
        self.drive_stop_time = datetime.now() + timedelta(milliseconds=duration)
        set_motor_speed(left_speed, right_speed)
    

    def outer_turn_right(self):
        self.tasks = [self._post_turn, self._turn_right, self._pre_turn]

   
    def outer_turn_left(self):
        self.tasks = [self._post_turn, self._turn_left, self._pre_turn]

   
    def inner_turn_left(self):
        self.tasks = [self._turn_left]

   
    def inner_turn_right(self):
        self.tasks = [self._turn_right]

   
    def stop(self):
        set_motor_speed(0, 0)


    #Not intended for public use

    def _turn_left(self):
        print('turn left')
        self.drive(-TURN_SPEED, TURN_SPEED, TURN_TIME)

  
    def _turn_right(self):
        print('turn right')
        self.drive(TURN_SPEED, -TURN_SPEED, TURN_TIME)
   
   
    def _post_turn(self):
        print('post turn')
        self.drive(25, 25, 700)

    def _pre_turn(self):
        print('pre turn')
        self.drive(25, 25, 500)