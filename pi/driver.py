from datetime import datetime, timedelta
from outbound import set_motor_speed

###### METHODS FOR CONTROLLING THE WHEELS #######	
# Tasks should be reversed since we pop them from the list 

TURN_SPEED = 45
TURN_TIME = 900
TURN_DEGREES = 90

class Driver:

    def __init__(self, gyro):
        self.drive_stop_time = 0
        self.tasks = []
        self.task = Task(None, (lambda: True))
        self.gyro = gyro
        self.previous_time = datetime.now()
        self.total_degrees = 0


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
            

    def driving(self):
        print("driving")
        return self.drive_stop_time <= datetime.now()


    def turning(self):
        print("Turning")
        data = self.gyro.read_data()

        if data == -1:
            raise Exception('Error reading gyro')

        time_delta = (self.previous_time - datetime.now()).total_seconds()
        delta_degrees = data * time_delta
        self.previous_time = datetime.now()        
        self.total_degrees += delta_degrees
        print('total degrees turned :' + str(self.total_degrees))

        return abs(self.total_degrees) >= 90


    def drive(self, left_speed, right_speed, duration):
        self.drive_stop_time = datetime.now() + timedelta(milliseconds=duration)
        set_motor_speed(left_speed, right_speed)


    def outer_turn_right(self):
        print('outer turn right')
        self.tasks = [Task(self._post_turn, self.driving), 
                      Task(self._turn_right, self.turning), 
                      Task(self._pre_turn, self.driving)]

   
    def outer_turn_left(self):
        print('outer turn left')
        self.tasks = [Task(self._post_turn, self.driving), 
                      Task(self._turn_left, self.turning), 
                      Task(self._pre_turn, self.driving)]

   
    def inner_turn_left(self):
        print('inner turn left')
        self.tasks = [Task(self._turn_left, self.turning)]

   
    def inner_turn_right(self):
        print('inner turn right')
        self.tasks = [Task(self._turn_right, self.turning)]

    
    def start(self):
        print('starting')
        self.tasks = [Task((lambda: self.drive(0, 0, 2000)), self.driving)]


    def stop(self):
        print('stopping')
        set_motor_speed(0, 0)


    #Not intended for public use

    def _turn_left(self):
        print('turn left')
        self.total_degrees = 0
        self.previous_time = datetime.now()
        self.drive(-TURN_SPEED, TURN_SPEED, TURN_TIME)


    def _turn_right(self):
        print('turn right')
        self.total_degrees = 0
        self.previous_time = datetime.now()
        self.drive(TURN_SPEED, -TURN_SPEED, TURN_TIME)


    def _post_turn(self):
        print('post turn')
        self.drive(25, 25, 700)


    def _pre_turn(self):
        print('pre turn')
        self.drive(25, 25, 500)




class Task:
    
    
    def __init__(self, task_func, done_func):
        self.task_func = task_func
        self.done_func = done_func


    def start(self):
        self.task_func()


    def done(self):
        return self.done_func()
