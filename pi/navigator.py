"""
State machine for navigational states
"""

from autocontroller import AutoController
from eventbus import EventBus
from protocol import CMD_TURN_STARTED, CMD_TURN_FINISHED

TURN_DIRECTION_RIGHT = True
TURN_DIRECTION_LEFT = False


class State:

    def run(self, data):
        assert 0, "run not implemented"

    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        assert 0, "sensor_data_received not implemented"


class auto_control(State):

    auto_controller = AutoController()

    def is_at_left_turn(self, data):
        diff = abs(data['ir_left'] - data['old_ir_left'])
        return diff >= Navigator.DISCONTINUITY_DIST and data['side'] == Navigator.LEFT_SIDE


    def is_at_right_turn(self, data):
        right_diff = abs(data['ir_right'] - data['old_ir_right'])
        return right_diff >= Navigator.DISCONTINUITY_DIST and data['side'] == Navigator.RIGHT_SIDE
            
        
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
       
        if self.is_at_left_turn(data) or self.is_at_right_turn(data):
            return

        right_speed, left_speed, regulation = auto_control.auto_controller.auto_control(new_ir_left, new_ir_right, data['side'])
        
        if abs(regulation) >= 33:
            print("Regulation to high: " + str(regulation))
            return 
            
        data['driver'].drive(left_speed, right_speed)
        
    def run(self, data):
        left_diff = data['ir_left'] - data['old_ir_left']
        right_diff = data['ir_right'] - data['old_ir_right']
        
        #print('ir right:' + str(data['ir_right']) + ' old ir right: ' + str(data['old_ir_right']) + ' right diff : ' + str(right_diff))
        #Outer turn, prioritize following right wall
        if self.is_at_right_turn(data):
            data['driver'].outer_turn_right()
            print('outer turn right')
            return turn(TURN_DIRECTION_RIGHT)
        
        if self.is_at_left_turn(data):
            data['driver'].outer_turn_left()
            print('outer turn left')
            return turn(TURN_DIRECTION_LEFT)
        
        laser_data = data['laser'].read_data()
        #print('Left diff: ' + str(left_diff) + ' right diff ' + str(right_diff))
        #print('laser distance: ' + str(laser_data))
        
        #Inner turn
        if laser_data <= Navigator.FACING_WALL_DIST and laser_data != -1:
            print("laserdata: "+ str(laser_data))
            if data['side'] == Navigator.LEFT_SIDE:
                data['driver'].inner_turn_right()
                print('inner turn right')
                return turn(TURN_DIRECTION_RIGHT)
            if data['side'] == Navigator.RIGHT_SIDE:
                data['driver'].inner_turn_left()
                print('inner turn left')
                return turn(TURN_DIRECTION_LEFT)
                
        return auto_control()


class warmup(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return #Do nothing
        
    def run(self, data):
        if data['driver'].idle():
            print('changin to auto control')
            return auto_control()
        else:
            return warmup()


class turn(State):
    def __init__(self, is_right_turn):
        self.is_right_turn = is_right_turn

    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return #Do nothing. Only auto control uses it

    def run(self, data):
        if data['driver'].idle():
            print('changing to auto control')
            return auto_control()
        else:
            return turn(self.is_right_turn)

###### NAVIGATOR CLASS #######
class Navigator:
    LEFT_SIDE = 0
    RIGHT_SIDE = 1

    DISCONTINUITY_DIST = 20.0 #mm
    FACING_WALL_DIST = 150 #mm

    def __init__(self, driver, laser):
        self.data = {'ir_left': 0,
                    'ir_right': 0,
                    'old_ir_right': 0,
                    'old_ir_left': 0,
                    'driver' : driver,
                    'laser' : laser,
                    'side' : Navigator.RIGHT_SIDE
                    }

        #Stand still waiting for sensors

        self.data['driver'].warmup()
        self.state = warmup()


    def sensor_data_received(self, new_ir_left, new_ir_right):
        self.data['old_ir_left'] = self.data['ir_left']
        self.data['old_ir_right'] = self.data['ir_right']
        self.data['ir_left'] = new_ir_left
        self.data['ir_right'] = new_ir_right
        self.state.sensor_data_received(self.data, new_ir_left, new_ir_right)
        
    #Runs the state. The states run method returns the next state
    def navigate(self):
        next_state = self.state.run(self.data)

        curr_type = type(self.state)
        next_type = type(next_state)

        if curr_type is not turn and next_type is turn:
            EventBus.notify(CMD_TURN_STARTED)

        if curr_type is turn and next_type is not turn:
            EventBus.notify(CMD_TURN_FINISHED, self.state.is_right_turn)

        self.state = next_state