from datetime import datetime, timedelta
from outbound import set_motor_speed

###### METHODS FOR CONTROLLING THE WHEELS #######	
# Tasks should be reversed since we pop them from the list 

STANDARD_SPEED = 25
TURN_SPEED = 45
TURN_TIME = 900
TURN_DEGREES = 90
POST_TURN_TIME = 700
PRE_TURN_TIME = 500
WARMUP_TIME = 2000

class Driver:

    def __init__(self, gyro):
        self.tasks = []
        self.task = Task(None, lambda: True)
        self.gyro = gyro


    def idle(self):
        if not self.task.done():
            print("Task Done")
            return False
        elif self.tasks:
            print("Popping taaaaasks")
            self.task = self.tasks.pop()
            self.task.start()
            return False
        else:
            print("STANNA")
            self.stop()
            return True
            

    def drive(self, left_speed, right_speed):
        set_motor_speed(left_speed, right_speed)


    def outer_turn_right(self):
        print('outer turn right')
        self.tasks = [DriveTask(self._post_turn, POST_TURN_TIME), 
                      TurnTask(self._turn_right, TURN_DEGREES, self.gyro), 
                      DriveTask(self._pre_turn, PRE_TURN_TIME)]

   
    def outer_turn_left(self):
        print('outer turn left')
        self.tasks = [DriveTask(self._post_turn, POST_TURN_TIME), 
                      TurnTask(self._turn_left, TURN_DEGREES, self.gyro), 
                      DriveTask(self._pre_turn, PRE_TURN_TIME)]

   
    def inner_turn_left(self):
        print('inner turn left')
        self.tasks = [TurnTask(self._turn_left, TURN_DEGREES, self.gyro)]

   
    def inner_turn_right(self):
        print('inner turn right')
        self.tasks = [TurnTask(self._turn_right, TURN_DEGREES, self.gyro)]

    
    def warmup(self):
        print('warming up')
        self.tasks = [DriveTask(lambda: self.drive(0, 0), WARMUP_TIME)]


    def stop(self):
        print('stopping')
        set_motor_speed(0, 0)


    #Not intended for public use

    def _turn_left(self):
        print('turn left')
        self.drive(-TURN_SPEED, TURN_SPEED)


    def _turn_right(self):
        print('turn right')
        self.drive(TURN_SPEED, -TURN_SPEED)


    def _post_turn(self):
        print('post turn')
        self.drive(STANDARD_SPEED, STANDARD_SPEED)


    def _pre_turn(self):
        print('pre turn')
        self.drive(STANDARD_SPEED, STANDARD_SPEED)



class Task:
    
    
    def __init__(self, task_func, done_func):
        self.task_func = task_func
        self.done_func = done_func


    def start(self):
        self.task_func()


    def done(self):
        return self.done_func()

class DriveTask(Task):
    

    def __init__(self, task_func, duration):
        Task.__init__(self, task_func, self.driving)
        self.duration = duration


    def start(self):
        Task.start(self)
        self.stop_time = datetime.now() + timedelta(milliseconds=self.duration)


    def driving(self):
        return self.stop_time <= datetime.now()


class TurnTask(Task):

    
    def __init__(self, task_func, degrees, gyro):
        Task.__init__(self, task_func, self.turning)
        self.degrees = degrees
        self.gyro = gyro
        
        
    def start(self):
        Task.start(self)
        self.previous_time = datetime.now()
        
    
    def turning(self):
        data = self.gyro.read_data()

        if data == -1:
            raise Exception('Error reading gyro')
        
        time_delta = (self.previous_time - datetime.now()).total_seconds()
        delta_degrees = data * time_delta
        self.previous_time = datetime.now()        
        self.total_degrees += delta_degrees
        print('total degrees turned :' + str(self.total_degrees))

        return abs(self.total_degrees) >= self.degrees

