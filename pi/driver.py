"""
Methods for controlling the wheels
"""

from datetime import datetime, timedelta

import math

import autocontroller
from outbound import set_motor_speed

###### METHODS FOR CONTROLLING THE WHEELS #######	
# Tasks should be reversed since we pop them from the list 

STANDARD_SPEED = 50
FAST_SPEED = 70
SLOW_SPEED = 40

TURN_SPEED = 40
TURN_TIME = 900
TURN_DEGREES = 80
POST_TURN_TIME = 700
PRE_TURN_TIME = 500
WARMUP_TIME = 2000
POST_TURN_DISTANCE = 200
PRE_TURN_DISTANCE = 200
REMOTE_COMMAND_EXECUTE_TIME = 525

"""
Thoughts on post_turn distance:

It appears that after a turn (at least on the track created yesterday) the laser will set a
destination at around 900 in start, but then as soon as it starts running distance_task
the laser values jumps up to 1300, and therefore it will travel too far before begining
to auto control. Not sure if it reads the laser value too soon, as in before it has finished
turning and instead reads a value on a wall to the side instead of the opposite wall, or if
it's something else. But that apprears to be the problem, and only when the distance is quite
far, >1m or so.
"""


class Driver:
    def __init__(self, gyro, laser):
        self.drive_stop_time = 0
        self.tasks = []
        self.task = Task(None, lambda: True)
        self.gyro = gyro
        self.laser = laser
        self.right_speed = 0
        self.left_speed = 0

    #Returns true only if we have executed all provided tasks
    def idle(self):
        return self.task.done() and not self.tasks

    #Expected to be run every main loop. Checks whether the current task is 
    #done, and if there are more to perform, starts performing them.
    def update(self):
        if self.task.done():
            if self.tasks:
                self.task = self.tasks.pop()
                print("Next task: " + str(self.task))
                self.task.start()
            else:
                #print("STANNA")
                self.stop()
            
    def drive(self, left_speed, right_speed):
        self.left_speed = left_speed
        self.right_speed = right_speed
        set_motor_speed(left_speed, right_speed)
        # print("Driver drive set motor speed to ", left_speed, right_speed)

    def outer_turn_right(self):
        print('outer turn right')
        self.task = Task(None, lambda: True)
        self.tasks = [DegreeTask(self._turn_right, TURN_DEGREES, self.gyro)]

    def outer_turn_left(self):
        print('outer turn left')
        self.task = Task(None, lambda: True)
        self.tasks = [DistanceTask(self._post_turn, POST_TURN_DISTANCE, self.laser),
                      DegreeTask(self._turn_left, TURN_DEGREES, self.gyro),
                      DistanceTask(self._pre_turn, PRE_TURN_DISTANCE, self.laser)]

    def inner_turn_left(self):
        print('inner turn left')
        current_degree = math.atan(autocontroller.last_diff / 165)
        degree = TURN_DEGREES - current_degree

        print('Current degree:', current_degree)
        print('Turning degree:', degree)

        self.task = Task(None, lambda: True)
        self.tasks = [DegreeTask(self._turn_left, degree, self.gyro)]

    def inner_turn_right(self):
        print('inner turn right')
        self.task = Task(None, lambda: True)
        self.tasks = [DegreeTask(self._turn_right, TURN_DEGREES, self.gyro)]

    def warmup(self):
        print('warming up')
        self.tasks = [TimedTask(lambda: self.drive(0, 0), WARMUP_TIME)]

    def stop(self):
        #print('stopping')
        self.drive(0, 0)

    def get_right_speed(self):
        return self.right_speed

    def get_left_speed(self):
        return self.left_speed


    # Commands intended to be called while remote controlling
         
    def drive_forward(self):
        self.task = TimedTask(self._drive_forward, REMOTE_COMMAND_EXECUTE_TIME)
        self.task.start()
    
    def drive_backward(self):
        self.task = TimedTask(self._drive_backward, REMOTE_COMMAND_EXECUTE_TIME)
        self.task.start()
        
    def turn_left(self):
        self.task = TimedTask(self._turn_left, REMOTE_COMMAND_EXECUTE_TIME)
        self.task.start()
        
    def turn_right(self):
        self.task = TimedTask(self._turn_right, REMOTE_COMMAND_EXECUTE_TIME)
        self.task.start()
        
    def drive_forward_right(self):
        self.task = TimedTask(self._drive_forward_right, REMOTE_COMMAND_EXECUTE_TIME)
        self.task.start()
        
    def drive_forward_left(self):
        self.task = TimedTask(self._drive_forward_left, REMOTE_COMMAND_EXECUTE_TIME)
        self.task.start()

    # Not intended for public use

    def _turn_left(self):
        print('turn left')
        self.drive(-TURN_SPEED, TURN_SPEED)

    def _turn_right(self):
        print('turn right')
        self.drive(TURN_SPEED, -TURN_SPEED)

    def _drive_forward(self):
        print('drive forward')
        self.drive(STANDARD_SPEED, STANDARD_SPEED)

    def _drive_backward(self):
        print('drive backward')
        self.drive(-STANDARD_SPEED, -STANDARD_SPEED)

    def _drive_forward_right(self):
        print('drive forward right')
        self.drive(FAST_SPEED, SLOW_SPEED)

    def _drive_forward_left(self):
        print('drive backward left')
        self.drive(SLOW_SPEED, FAST_SPEED)
        
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


class TimedTask(Task):
    def __init__(self, task_func, duration):
        Task.__init__(self, task_func, self.timed_task)
        self.duration = duration
        self.stop_time = datetime.now()

    def start(self):
        Task.start(self)
        self.stop_time = datetime.now() + timedelta(milliseconds=self.duration)
        print("Start timed task")

    def timed_task(self):
        #print('time left driving: ' + str(self.stop_time - datetime.now()))
        return self.stop_time <= datetime.now()


class DegreeTask(Task):
    def __init__(self, task_func, degrees, gyro):
        Task.__init__(self, task_func, self.degree_task)
        self.total_degrees = 0
        self.previous_time = datetime.now()
        self.degrees = degrees
        self.gyro = gyro

    def start(self):
        self.total_degrees = 0
        self.previous_time = datetime.now()
        Task.start(self)


    def degree_task(self):
        data = self.gyro.get_data()

        if data == -1:
            raise Exception('Error reading gyro')

        time_delta = (self.previous_time - datetime.now()).total_seconds()
        delta_degrees = data * time_delta
        #print("time_delta: " + str(time_delta))
        #print("delta_degrees: " + str(delta_degrees))
        self.previous_time = datetime.now()
        self.total_degrees += delta_degrees
        #print('total degrees turned :' + str(self.total_degrees))

        return abs(self.total_degrees) >= self.degrees


class DistanceTask(Task):
    def __init__(self, task_func, distance, laser):
        Task.__init__(self, task_func, self.distance_task)
        self.destination = 0
        self.previous_time = datetime.now()
        self.distance = distance
        self.laser = laser

    def start(self):
        laser_data = -1
        while laser_data == -1:
            laser_data = self.laser.get_data()
            print("RUN RUN RUN LASER READINGS")

        #print("Distance: " + str(self.distance))
        #print("Laser data: " + str(laser_data))

        self.destination = laser_data - self.distance
        #print("Destination: " + str(self.destination))
        self.previous_time = datetime.now()
        Task.start(self)

    def distance_task(self):
        laser_data = -1
        while laser_data == -1:
            laser_data = self.laser.get_data()

        return self.destination >= laser_data

