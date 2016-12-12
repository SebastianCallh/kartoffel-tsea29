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


class AutoControl(State):
    auto_controller = AutoController()

    def is_at_right_turn(self, data):
        return data['ir'].get_ir_right() == -1 and \
               data['ir'].get_ir_right_back() == -1 and \
               Navigator.right_turn_enabled

    def run(self, data):

        if self.is_at_right_turn(data):
            data['driver'].outer_turn_right()
            print('NAVIGATOR: outer turn right')
            return Turn(TURN_DIRECTION_RIGHT)

        laser_data = data['laser'].get_data()

        if not Navigator.right_turn_enabled:
            Navigator.right_turn_enabled = (data['ir'].get_ir_right() != -1 and data['ir'].get_ir_right_back() != -1)

        # Inner turn
        if Navigator.force_left_turn or (laser_data <= Navigator.FACING_WALL_DIST and laser_data != -1 and (not Navigator.right_turn_enabled or data['ir'].get_ir_right() != -1)):
            Navigator.force_left_turn = False
            if data['side'] == Navigator.RIGHT_SIDE:
                data['driver'].inner_turn_left()
                print('NAVIGATOR: inner turn left')
                return Turn(TURN_DIRECTION_LEFT)

        right_speed, left_speed, regulation = AutoControl.auto_controller.auto_control(data['ir'].get_ir_right(),
                                                                                       data['ir'].get_ir_right_back(),
                                                                                       data['side'])
        data['driver'].drive(left_speed, right_speed)

        return self


class Warmup(State):
    def run(self, data):
        if data['driver'].idle():
            print('NAVIGATOR: changin to auto control')
            return AutoControl()
        else:
            return self


class Turn(State):
    def __init__(self, is_right_turn):
        self.is_right_turn = is_right_turn

    def run(self, data):
        if Navigator.right_turn_enabled:
            Navigator.right_turn_enabled = False

        if data['driver'].idle():
            print('NAVIGATOR: changing to auto control')
            return AutoControl()
        else:
            return self


###### NAVIGATOR CLASS #######
class Navigator:
    LEFT_SIDE = 0
    RIGHT_SIDE = 1

    MANUAL = 0
    AUTONOMOUS = 1
    
    DISCONTINUITY_DIST = 25.0  # mm
    FACING_WALL_DIST = 200  # mm

    right_turn_enabled = True
    force_left_turn = False

    def __init__(self, mode, ir, driver, laser):
        self.data = {
            'driver': driver,
            'laser': laser,
            'ir': ir,
            'side': Navigator.RIGHT_SIDE,
        }
        self.mode = mode
        self.state = Warmup()
        self.last_updated_time = datetime.now()

        # Stand still waiting for sensors
        self.data['driver'].warmup()
        
    # Runs the state. The states run method returns the next state
    def navigate(self):
        self.data['driver'].update()
        if self.mode == Navigator.AUTONOMOUS:
            next_state = self.state.run(self.data)

            curr_type = type(self.state)
            next_type = type(next_state)

            if curr_type is not Turn and next_type is Turn:
                EventBus.notify(CMD_TURN_STARTED)

            if curr_type is Turn and next_type is not Turn:
                EventBus.notify(CMD_TURN_FINISHED, self.state.is_right_turn)

            self.state = next_state
            
    def drive_forward(self):
        if self.mode == Navigator.MANUAL:
            self.data['driver'].drive_forward()
    
    def drive_backward(self):
        if self.mode == Navigator.MANUAL:
            self.data['driver'].drive_backward()
           
    def drive_forward_right(self):
        if self.mode == Navigator.MANUAL:
            self.data['driver'].drive_forward_right()
    
    def drive_forward_left(self):
        if self.mode == Navigator.MANUAL:
            self.data['driver'].drive_forward_left()

    def turn_left(self):
        if self.mode == Navigator.MANUAL:
            self.data['driver'].turn_left()
        
    def turn_right(self):
        if self.mode == Navigator.MANUAL:
            self.data['driver'].turn_right()
        
    def set_mode(self, mode):
        self.mode = mode