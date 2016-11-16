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
        self.tasks = [self._nudge_forward, self._turn_right, self._nudge_forward]

   
    def outer_turn_left(self):
        self.tasks = [self._nudge_forward, self._turn_left, self._nudge_forward]

   
    def inner_turn_left(self):
        self.tasks = [self._turn_left]

   
    def inner_turn_right(self):
        self.tasks = [self._turn_right]

   
    def stop(self):
        set_motor_speed(0, 0)


    #Not intended for public use

    def _turn_left(self):
        self.drive(-TURN_SPEED, TURN_SPEED, TURN_TIME)

  
    def _turn_right(self):
        self.drive(TURN_SPEED, -TURN_SPEED, TURN_TIME)
   

    def _nudge_forward(self):
        self.drive(20, 20, 800)