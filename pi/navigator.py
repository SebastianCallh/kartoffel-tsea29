from autocontroller import AutoController

###### STATE MACHINE FOR NAVIGATIONAL STATES ########



class State:
    def run(self):
        assert 0, "run not implemented"
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        assert 0, "sensor_data_received not implemented"

class auto_control(State):

    auto_controller = AutoController()

    def is_at_left_turn(self, data):
        diff = data['ir_left'] - data['old_ir_left']
        return diff >= Navigator.DISCONTINUITY_DIST and data['side'] == Navigator.LEFT_SIDE


    def is_at_right_turn(self, data):
        right_diff = data['ir_right'] - data['old_ir_right']
        return right_diff >= Navigator.DISCONTINUITY_DIST and data['side'] == Navigator.RIGHT_SIDE
            
        
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
       
        if self.is_at_left_turn(data) or self.is_at_right_turn(data):
            return
        
        right_speed, left_speed, regulation = auto_control.auto_controller.auto_control(new_ir_left, new_ir_right, data['side'])
        
        if abs(regulation) >= 30: 
            return 
            
        #Duration set to something quite high to mimic running forever (until next update)
        data['driver'].drive(left_speed, right_speed, 500)
        
    def run(self, data):
        left_diff = data['ir_left'] - data['old_ir_left']
        right_diff = data['ir_right'] - data['old_ir_right']
        
        print('ir right:' + str(data['ir_right']) + ' old ir right: ' + str(data['old_ir_right']) + ' right diff : ' + str(right_diff))
        #Outer turn, prioritize following right wall
        if self.is_at_right_turn(data):
            data['driver'].outer_turn_right()
            print('outer turn right')
            return turn()
        
        if self.is_at_left_turn(data):
            data['driver'].outer_turn_left()
            print('outer turn left')
            return turn()
        
        print('Left diff: ' + str(left_diff) + ' right diff ' + str(right_diff))
        print('laser distance: ' + str(data['laser'].read_data()))
        
        #Inner turn
        if data['laser'].read_data() <=  Navigator.FACING_WALL_DIST && data['laser'] != -1:
            if data['side'] == Navigator.LEFT_SIDE:
                data['driver'].inner_turn_right()
                print('inner turn right')
                return turn()
            if data['side'] == Navigator.RIGHT_SIDE:
                data['driver'].inner_turn_left()
                print('inner turn left')
                return turn()
                
        return auto_control()

class warmup(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return #Do nothing
        
    def run(self, data):
        if not data['driver'].driving():
            return auto_control()
        else:
            return warmup()

class turn(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return #Do nothing. Only auto control uses it

    def run(self, data):
        if not data['driver'].driving():
            print('changing to auto control')
            return auto_control()
        else:
            return turn()

###### NAVIGATOR CLASS #######	
class Navigator:

    LEFT_SIDE = 0
    RIGHT_SIDE = 1

    DISCONTINUITY_DIST = 8.0 #mm
    FACING_WALL_DIST = 200 #mm

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
        self.data['driver'].drive(0, 0, 2000)
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
        self.state = next_state