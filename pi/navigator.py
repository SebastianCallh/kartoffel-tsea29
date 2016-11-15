from autocontroller import AutoController

###### STATE MACHINE FOR NAVIGATIONAL STATES ########

class State:
    def run(self):
        assert 0, "run not implemented"
    def sensor_data_received(self, data, new_ir_right, new_ir_left):
        assert 0, "sensor_data_received not implemented"
		
class auto_control(State):
	
	auto_controller = AutoController()
	
	def sensor_data_received(self, data, new_ir_right, new_ir_left):
		##NOTE TO SELF: Kan inte reglera pa vanster sida nu!!!
		right_speed, left_speed = auto_control.auto_controller.auto_control(new_ir_right, new_ir_left, 'right')
		#Duration set to something quite high to mimic running forever (until next update)
		data['driver'].drive(left_speed, right_speed, 500)
		
	def run(self, data):
		#If sensor readings jump more than 5 mm we've discovered a turn
		return auto_control()
		DISCONTINUITY_DIST = 5.0
		if data['ir_right'] - data['old_ir_right'] >= DISCONTINUITY_DIST:
			data['driver'].prepare_for_turn()
			return before_turn()
		else:
			return auto_control()
		
		
class before_turn(State):
	def sensor_data_received(self, data, new_ir_right, new_ir_left):
		return #Do nothing. Only auto control uses it
	
	def run(self, data):
		if not data['driver'].driving:
			data['driver'].turn_right()
			return turn()
		else:
			return before_turn()
	
class turn(State):
	def sensor_data_received(self, data, new_ir_right, new_ir_left):
		return #Do nothing. Only auto control uses it
	
	def run(self, data):
		if not data['driver'].driving:
			return auto_control()
		else:
			return turn()
		
###### NAVIGATOR CLASS #######	
class Navigator:

	def __init__(self, driver):
		self.driver = driver
		self.state = auto_control()
		self.data = {'ir_left': 0,
					'ir_right': 0,
					'old_ir_right': 0,
					'old_ir_left': 0,
					'driver' : driver
					}
						
	def sensor_data_received(self, new_ir_right, new_ir_left):
		self.state.sensor_data_received(self.data, new_ir_left, new_ir_right)
		self.data['old_ir_left'] = self.data['ir_left']
		self.data['old_ir_right'] = self.data['ir_right']
		self.data['ir_left'] = new_ir_left
		self.data['ir_right'] = new_ir_right
		
	#Runs the state. The states run method returns the next state
	def navigate(self):
		self.state = self.state.run(self.data)