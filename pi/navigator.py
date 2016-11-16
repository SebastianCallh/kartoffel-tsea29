"""
State machine for navigational states
"""

from autocontroller import AutoController


class State:
    def run(self, data):
        assert 0, "run not implemented"

    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        assert 0, "sensor_data_received not implemented"


class AutoControl(State):
    auto_controller = AutoController()

    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        # NOTE: Kan inte reglera pa vanster sida nu!!!
        right_speed, left_speed = AutoControl.auto_controller.auto_control(
            new_ir_left, new_ir_right, 'right')
        # Duration set to something quite high to mimic running forever (until
        # next update)
        data['driver'].drive(left_speed, right_speed, 500)

    def run(self, data):
        # If sensor readings jump more than 5 mm we've discovered a turn
        print('distance diff: ' + str(data['ir_right'] - data['old_ir_right']))
        print('laser distance: ' + str(data['laser'].read_data()))
        DISCONTINUITY_DIST = 20.0  # mm
        if data['ir_right'] - data['old_ir_right'] >= DISCONTINUITY_DIST:
            print('changing to preparing for turn')
            data['driver'].prepare_for_turn()
            return BeforeTurn()
        else:
            return AutoControl()


class Warmup(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return  # Do nothing

    def run(self, data):
        if not data['driver'].driving():
            return AutoControl()
        else:
            return Warmup()


class BeforeTurn(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return  # Do nothing. Only auto control uses it

    def run(self, data):
        print('running before turn')
        if not data['driver'].driving():
            print('changing to turn')
            data['driver'].turn_right()
            return Turn()
        else:
            return BeforeTurn()


class AfterTurn(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return  # Do nothing. Only auto control uses it

    def run(self, data):
        print('running after turn')
        if not data['driver'].driving():
            print('changing to auto control')
            return AutoControl()
        else:
            return AfterTurn()


class Turn(State):
    def sensor_data_received(self, data, new_ir_left, new_ir_right):
        return  # Do nothing. Only auto control uses it

    def run(self, data):
        if not data['driver'].driving():
            print('changing to after turn')
            data['driver'].prepare_for_turn()
            return AfterTurn()
        else:
            return Turn()


class Navigator:
    def __init__(self, driver, laser):
        self.data = {'ir_left': 0,
                     'ir_right': 0,
                     'old_ir_right': 0,
                     'old_ir_left': 0,
                     'driver': driver,
                     'laser': laser
                     }

        # Stand still for 100 ms, waiting for sensors
        self.data['driver'].drive(0, 0, 1000)
        self.state = Warmup()

    def sensor_data_received(self, new_ir_left, new_ir_right):
        self.state.sensor_data_received(self.data, new_ir_left, new_ir_right)
        self.data['old_ir_left'] = self.data['ir_left']
        self.data['old_ir_right'] = self.data['ir_right']
        self.data['ir_left'] = new_ir_left
        self.data['ir_right'] = new_ir_right

    # Runs the state. The states run method returns the next state
    def navigate(self):
        next_state = self.state.run(self.data)
        self.state = next_state
