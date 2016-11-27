"""
Methods for controlling the wheels
"""

from datetime import datetime, timedelta
from outbound import set_motor_speed

###### METHODS FOR CONTROLLING THE WHEELS #######	
# Tasks should be reversed since we pop them from the list 

STANDARD_SPEED = 25
TURN_SPEED = 45
TURN_TIME = 900
TURN_DEGREES = 80
POST_TURN_TIME = 700
PRE_TURN_TIME = 500
WARMUP_TIME = 2000
POST_TURN_DISTANCE = 200
PRE_TURN_DISTANCE = 200


class Driver:
    def __init__(self, gyro, laser):
        self.drive_stop_time = 0
        self.tasks = []
        self.task = Task(None, lambda: True)
        self.gyro = gyro
        self.laser = laser

    def idle(self):
        if not self.task.done():
            print("Task not done")
            return False
        elif self.tasks:
            self.task = self.tasks.pop()
            print("Next task: " + str(self.task))
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
        self.tasks = [DistanceTask(self._post_turn, POST_TURN_DISTANCE, self.laser),
                      DegreeTask(self._turn_right, TURN_DEGREES, self.gyro),
                      DistanceTask(self._pre_turn, PRE_TURN_DISTANCE, self.laser)]

    def outer_turn_left(self):
        print('outer turn left')
        self.tasks = [DistanceTask(self._post_turn, POST_TURN_DISTANCE, self.laser),
                      DegreeTask(self._turn_left, TURN_DEGREES, self.gyro),
                      DistanceTask(self._pre_turn, PRE_TURN_DISTANCE, self.laser)]

    def inner_turn_left(self):
        print('inner turn left')
        self.tasks = [DegreeTask(self._turn_left, TURN_DEGREES, self.gyro)]

    def inner_turn_right(self):
        print('inner turn right')
        self.tasks = [DegreeTask(self._turn_right, TURN_DEGREES, self.gyro)]

    def warmup(self):
        print('warming up')
        self.tasks = [TimedTask(lambda: self.drive(0, 0), WARMUP_TIME)]

    def stop(self):
        print('stopping')
        set_motor_speed(0, 0)

    # Not intended for public use

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


class TimedTask(Task):
    def __init__(self, task_func, duration):
        Task.__init__(self, task_func, self.timed_task)
        self.duration = duration
        self.stop_time = datetime.now()

    def start(self):
        Task.start(self)
        self.stop_time = datetime.now() + timedelta(milliseconds=self.duration)

    def timed_task(self):
        print('time left driving: ' + str(self.stop_time - datetime.now()))
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
        data = self.gyro.read_data()

        if data == -1:
            raise Exception('Error reading gyro')

        time_delta = (self.previous_time - datetime.now()).total_seconds()
        delta_degrees = data * time_delta
        #print("time_delta: " + str(time_delta))
        #print("delta_degrees: " + str(delta_degrees))
        self.previous_time = datetime.now()
        self.total_degrees += delta_degrees
        print('total degrees turned :' + str(self.total_degrees))

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
            laser_data = self.laser.read_data()
            print("RUN RUN RUN LASER READINGS")

        self.destination = laser_data - self.distance
        self.previous_time = datetime.now()

        Task.start(self)

    def distance_task(self):

        laser_data = -1
        while laser_data == -1:
            laser_data = self.laser.read_data()
            #print("Distance Task Laser: " + str(laser_data - self.destination))

        return self.destination >= laser_data

