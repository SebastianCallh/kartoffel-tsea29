"""
State machine for navigational states
"""
from datetime import datetime, timedelta

from autocontroller import AutoController
from eventbus import EventBus
from protocol import CMD_TURN_STARTED, CMD_TURN_FINISHED

TURN_DIRECTION_RIGHT = True
TURN_DIRECTION_LEFT = False
UPDATE_FREQUENCY = 50

class State:
    def run(self, data):
        assert 0, "run not implemented"

    def sensor_data_received(self, data, new_ir_left, new_ir_right, new_ir_right_back_mm, new_ir_left_back_mm):
        assert 0, "sensor_data_received not implemented"


class AutoControl(State):
    auto_controller = AutoController()

    def is_at_left_turn(self, data):
        left_old_diff = abs(data['ir_left'] - data['old_ir_left'])
        left_new_diff = abs(data['new_ir_left'] - data['old_ir_left'])

        #print("At left turn, old diff: " + str(left_old_diff) + ", new diff: "+ str(left_new_diff))

        return left_old_diff >= Navigator.DISCONTINUITY_DIST and\
               left_new_diff >= Navigator.DISCONTINUITY_DIST and\
               data['side'] == Navigator.LEFT_SIDE

    def is_at_right_turn(self, data):
        return data['new_ir_right'] == -1 and \
               data['new_ir_right_back'] == -1 and \
               Navigator.right_turn_enabled
         
    def sensor_data_received(self, data, new_ir_left, new_ir_right, new_ir_right_back_mm, new_ir_left_back_mm):
       
        if self.is_at_left_turn(data) or self.is_at_right_turn(data):
            return

        right_speed, left_speed, regulation = AutoControl.auto_controller.auto_control(new_ir_right, new_ir_right_back_mm, data['side'])
        data['driver'].drive(left_speed, right_speed)

    def run(self, data):

        if self.is_at_right_turn(data):
            data['driver'].outer_turn_right()
            print('NAVIGATOR: outer turn right')
            return Turn(TURN_DIRECTION_RIGHT)

        if self.is_at_left_turn(data):
            data['driver'].outer_turn_left()
            print('NAVIGATOR: outer turn left')
            return Turn(TURN_DIRECTION_LEFT)

        laser_data = data['laser'].get_data()
        
        if (not Navigator.right_turn_enabled):
            Navigator.right_turn_enabled = (data['new_ir_right'] != -1 and data['new_ir_right_back'] != -1)
       
        # Inner turn
        if laser_data <= Navigator.FACING_WALL_DIST and laser_data != -1:
            
            if data['side'] == Navigator.LEFT_SIDE:
                data['driver'].inner_turn_right()
                print('NAVIGATOR: inner turn right')
                return Turn(TURN_DIRECTION_RIGHT)
                
            if data['side'] == Navigator.RIGHT_SIDE:
                data['driver'].inner_turn_left()
                print('NAVIGATOR: inner turn left')
                return Turn(TURN_DIRECTION_LEFT)

        return AutoControl()


class Warmup(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right, new_ir_right_back_mm, new_ir_left_back_mm):
        return #Do nothing
        
    def run(self, data):
        if data['driver'].idle():
            print('NAVIGATOR: changin to auto control')
            return AutoControl()
        else:
            return Warmup()


class Turn(State):
    def __init__(self, is_right_turn):
        self.is_right_turn = is_right_turn

    def sensor_data_received(self, data, new_ir_left, new_ir_right, new_ir_right_back_mm, new_ir_left_back_mm):
        return #Do nothing. Only auto control uses it

    def run(self, data):
        if Navigator.right_turn_enabled:
            Navigator.right_turn_enabled = False

        if data['driver'].idle():
            print('NAVIGATOR: changing to auto control')
            return AutoControl()
        else:
            return Turn(self.is_right_turn)


###### NAVIGATOR CLASS #######
class Navigator:
    LEFT_SIDE = 0
    RIGHT_SIDE = 1

    DISCONTINUITY_DIST = 25.0  # mm
    FACING_WALL_DIST = 200  # mm

    right_turn_enabled = True

    def __init__(self, driver, laser):
        self.data = {
                     'ir_left': 0,
                     'ir_right': 0,
                     'old_ir_right': 0,
                     'old_ir_left': 0,
                     'driver': driver,
                     'laser': laser,
                     'side': Navigator.RIGHT_SIDE,
                     'new_ir_right': 0,
                     'new_ir_left': 0
                    }

        #Stand still waiting for sensors
        self.data['driver'].warmup()
        self.state = Warmup()
        self.last_updated_time = datetime.now()


    def sensor_data_received(self, new_ir_left, new_ir_right, new_ir_right_back_mm, new_ir_left_back_mm):

        if datetime.now() - self.last_updated_time < timedelta(milliseconds=UPDATE_FREQUENCY):
            return

        self.data['old_ir_left'] = self.data['ir_left']
        self.data['old_ir_right'] = self.data['ir_right']
        self.data['ir_left'] = self.data['new_ir_left']
        self.data['ir_right'] = self.data['new_ir_right']
        self.data['new_ir_right'] = new_ir_right
        self.data['new_ir_left'] = new_ir_left
        self.data['new_ir_left_back'] = new_ir_left_back_mm
        self.data['new_ir_right_back'] = new_ir_right_back_mm

        if self.data['old_ir_right'] == -1 and self.data['ir_right'] == -1:
            self.data['ir_right'] = self.data['new_ir_right']
            self.data['old_ir_right'] = self.data['new_ir_right']

        self.state.sensor_data_received(self.data, new_ir_left, new_ir_right, new_ir_right_back_mm, new_ir_left_back_mm)
        self.last_updated_time = datetime.now()
        
    #Runs the state. The states run method returns the next state
    def navigate(self):
        next_state = self.state.run(self.data)

        curr_type = type(self.state)
        next_type = type(next_state)

        if curr_type is not Turn and next_type is Turn:
            EventBus.notify(CMD_TURN_STARTED)

        if curr_type is Turn and next_type is not Turn:
            EventBus.notify(CMD_TURN_FINISHED, self.state.is_right_turn)
            self.data['old_ir_left'] = self.data['new_ir_left']
            self.data['old_ir_right'] = self.data['new_ir_right']
            self.data['ir_left'] = self.data['new_ir_left']
            self.data['ir_right'] = self.data['new_ir_right']


        self.state = next_state
