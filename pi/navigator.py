from autocontroller import AutoController

###### STATE MACHINE FOR NAVIGATIONAL STATES ########

class State:
    def run(self):
        assert 0, "run not implemented"
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        assert 0, "sensor_data_received not implemented"
		
class auto_control(State):
	
	auto_controller = AutoController()
	
	def sensor_data_received(self, data, new_ir_left, new_ir_right):
		##NOTE TO SELF: Kan inte reglera pa vanster sida nu!!!
		right_speed, left_speed = auto_control.auto_controller.auto_control(new_ir_left, new_ir_right, 'right')
		#Duration set to something quite high to mimic running forever (until next update)
		data['driver'].drive(left_speed, right_speed, 500)
		
	def run(self, data):
		#If sensor readings jump more than 5 mm we've discovered a turn
		print('distance diff: ' + str(data['ir_right'] - data['old_ir_right']))
		print('laser distance: ' + str(data['laser'].read_data()))
		DISCONTINUITY_DIST = 20.0 #mm
		FACING_WALL_DIST = 30 #mm
		if data['ir_right'] - data['old_ir_right'] >= DISCONTINUITY_DIST:
			print('changing to preparing for turn')
			data['driver'].prepare_for_turn()
			return before_turn()
		#elif data['laser'].read_data() <=  FACING_WALL_DIST:
		#	data['driver'].turn_left()
		#	return turn()
		else:
			return auto_control()
				
class warmup(State):
	
	def sensor_data_received(self, data, new_ir_left, new_ir_right):
		return #Do nothing
		
	def run(self, data):
		if not data['driver'].driving():
			return auto_control()
		else:
			return warmup()
		
class before_turn(State):
	def sensor_data_received(self, data, new_ir_left, new_ir_right):
		return #Do nothing. Only auto control uses it
	
	def run(self, data):
		print('running before turn')
		if not data['driver'].driving():
			print('changing to turn')
			data['driver'].turn_right()
			return turn()
		else:
			return before_turn()

class after_turn(State):
	def sensor_data_received(self, data, new_ir_left, new_ir_right):
		return #Do nothing. Only auto control uses it
	
	def run(self, data):
		print('running after turn')
		if not data['driver'].driving():
			print('changing to auto control')
			return auto_control()
		else:
			return after_turn()			

	
class turn(State):
	def sensor_data_received(self, data, new_ir_left, new_ir_right):
		return #Do nothing. Only auto control uses it
	
	def run(self, data):
		if not data['driver'].driving():
			print('changing to after turn')
			data['driver'].prepare_for_turn()
			return after_turn()
		else:
			return turn()
		
###### NAVIGATOR CLASS #######	
class Navigator:

	def __init__(self, driver, laser):
		self.data = {'ir_left': 0,
					'ir_right': 0,
					'old_ir_right': 0,
					'old_ir_left': 0,
					'driver' : driver,
					'laser' : laser
					}
		
		#Stand still for 100 ms, waiting for sensors
		self.data['driver'].drive(0, 0, 1000)
		self.state = warmup()
		
	
	def sensor_data_received(self, new_ir_left, new_ir_right):
		self.state.sensor_data_received(self.data, new_ir_left, new_ir_right)
		self.data['old_ir_left'] = self.data['ir_left']
		self.data['old_ir_right'] = self.data['ir_right']
		self.data['ir_left'] = new_ir_left
		self.data['ir_right'] = new_ir_right
		
	#Runs the state. The states run method returns the next state
	def navigate(self):
		next_state = self.state.run(self.data)
		self.state = next_state