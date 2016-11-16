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
		right_speed, left_speed = auto_control.auto_controller.auto_control(new_ir_left, new_ir_right, data['side'])
		#Duration set to something quite high to mimic running forever (until next update)
		data['driver'].drive(left_speed, right_speed, 500)
		
	def run(self, data):
		left_diff = data['ir_left'] - data['old_ir_left']
		right_diff = data['ir_right'] - data['old_ir_right']
		
		#Outer turn, prioritize following right wall
		if right_diff >= Navigator.DISCONTINUITY_DIST and data['side'] == RIGHT_SIDE:
			data['driver'].outer_turn_right()
			return turn()
			
		if left_diff >= Navigator.DISCONTINUITY_DIST and data['side'] == LEFT_SIDE:
			data['driver'].outer_turn_left()
			return turn()
		
		print('Left distance: ' + str(left_distance) + ' right distance ' + str(right_distance))
		print('laser distance: ' + str(data['laser'].read_data()))
		
		#Inner turn
		if data['laser'].read_data() <=  Navigator.FACING_WALL_DIST:
			if data['side'] == LEFT_SIDE:
				data['driver'].inner_turn_right()
				return turn()
			if data['side'] == RIGHT_SIDE:
				data['driver'].inner_turn_left()
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
		
class outer_turn(State):
	def sensor_data_received(self, data, new_ir_left, new_ir_right):
		return #Do nothing. Only auto control uses it
	
	def run(self, data):
		print('running outer turn')
		if not data['driver'].driving():
			data['driver'].turn_right()
			return turn()
		else:
			return outer_turn()

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

	LEFT_SIDE = 0
	RIGHT_SIDE = 1

	DISCONTINUITY_DIST = 20.0 #mm
	FACING_WALL_DIST = 200 #mm
	
	def __init__(self, driver, laser):
		self.data = {'ir_left': 0,
					'ir_right': 0,
					'old_ir_right': 0,
					'old_ir_left': 0,
					'driver' : driver,
					'laser' : laser,
					'side' : RIGHT_SIDE
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