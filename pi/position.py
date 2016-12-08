from eventbus import EventBus
from laser import Laser
from protocol import CMD_TURN_STARTED, CMD_TURN_FINISHED
from section import Section, NORTH, EAST, SOUTH, WEST, BLOCK_LENGTH_MM
from threading import Thread

STATE_MEASURING = 0
STATE_WAITING = 1


class Position:
    def __init__(self, laser, ir):
        self.laser = laser
        self.ir = ir
        self.state = STATE_MEASURING
        self.current_section = Section(NORTH)
        self.saved_sections = []
        self.map_data = []
        self.current_x = 0
        self.current_y = 0

        self.kitchen_section = Section(NORTH)
        self.looking_for_kitchen = False
        self.kitchen_block_displacement = 0
        self.potential_kitchen = []
        self.temporary_potential_kitchen = []

        EventBus.subscribe(CMD_TURN_STARTED, self.on_turning_started)
        EventBus.subscribe(CMD_TURN_FINISHED, self.on_turning_finished)

    def update(self):
        if self.state == STATE_MEASURING:
            distance = self.laser.get_data()
            self.current_section.add_distance_sample(distance)

            # Checks if a kitchen island may be present and start calculating sections for it.
            if self.ir.get_ir_left() > 30 and not self.looking_for_kitchen:
                print("start for kitchen")
                self.looking_for_kitchen = True
                self.kitchen_section = Section(self.current_section.direction)
                self.temporary_potential_kitchen = []
                self.kitchen_section.add_distance_sample(distance)
                self.kitchen_block_displacement = 0

            elif self.ir.get_ir_left_back() > 250 and not self.looking_for_kitchen:
                print("start for kitchen long")
                self.looking_for_kitchen = True
                self.kitchen_section = Section(self.current_section.direction)
                self.temporary_potential_kitchen = []
                self.kitchen_section.add_distance_sample(distance)
                self.kitchen_block_displacement = 1

            elif (self.ir.get_ir_left() == -1 and self.kitchen_block_displacement == 0) or \
                 (self.ir.get_ir_left_back() == -1 and self.kitchen_block_displacement == 1) and self.looking_for_kitchen:
                self.kitchen_section.finish()
                self.looking_for_kitchen = False
                self.calculate_kitchen_coordinates()

    def save_current_section(self):
        self.current_section.finish()

        self.saved_sections.append(self.current_section)
        self.map_data.append(self.transform_map_data(self.current_section))

        if self.looking_for_kitchen:
            self.kitchen_section.finish()
            self.looking_for_kitchen = False
            self.calculate_kitchen_coordinates()

        print("Primary temporary kitchens: " + str(self.temporary_potential_kitchen))

        # Removes potential kitchens if already passed
        if self.potential_kitchen.count((self.current_x, self.current_y)) > 0:
            self.potential_kitchen.remove((self.current_x, self.current_y))

        # Adds all new potential kitchens.
        self.potential_kitchen = self.potential_kitchen + self.temporary_potential_kitchen

        print('---- SECTION SAVED ----')
        print('  direction: ' + str(self.current_section.direction))
        print('  distance: ' + str(self.current_section.block_distance))
        print('  coordinates: ' + str(self.current_x) + ", " + str(self.current_y))
        print('  potential kitchens: ' + str(self.potential_kitchen))
        print('-----------------------')

    def begin_next_section(self, is_right_turn):
        if is_right_turn:
            self.current_section = self.current_section.for_right_turn()
        else:
            self.current_section = self.current_section.for_left_turn()

    def on_turning_started(self):
        self.state = STATE_WAITING
        thread = Thread(target=self.save_current_section())
        thread.start()

    def on_turning_finished(self, is_right_turn):
        self.begin_next_section(is_right_turn)
        self.state = STATE_MEASURING

    def transform_map_data(self, section):
        if section.direction == NORTH:
            self.current_y += section.block_distance
        elif section.direction == EAST:
            self.current_x += section.block_distance
        elif section.direction == SOUTH:
            self.current_y -= section.block_distance
        elif section.direction == WEST:
            self.current_x -= section.block_distance
        return self.current_x, self.current_y

    '''
    Returns a list of tuples with coordinates of all the corners
    '''
    def get_map_data(self):
        return [self.map_data]

    '''
    Returns the robots last know x,y coordinates
    '''
    def get_current_position(self):
        return self.current_x, self.current_y

    def calculate_kitchen_coordinates(self):
        block_distance_from_turn = round((self.current_section.get_max() - self.kitchen_section.get_max()) /
                                         BLOCK_LENGTH_MM)
        print("Kitchen blockdistance from turn: " + str(block_distance_from_turn))

        kitchen_x = 0
        kitchen_y = 0

        # Transforms coordinates to match the kitchen island displacement
        if self.kitchen_section.direction == NORTH:
            kitchen_x -= self.kitchen_block_displacement
        elif self.kitchen_section.direction == EAST:
            kitchen_y += self.kitchen_block_displacement
        elif self.kitchen_section.direction == SOUTH:
            kitchen_x += self.kitchen_block_displacement
        elif self.kitchen_section.direction == WEST:
            kitchen_y -= self.kitchen_block_displacement

        # Sets the kitchens start position to the current + displacement
        kitchen_start_x = kitchen_x + self.current_x
        kitchen_start_y = kitchen_y + self.current_y

        # Adding in the direction the island was found
        if self.kitchen_section.direction == NORTH:
            kitchen_start_y += block_distance_from_turn
            kitchen_y += self.kitchen_section.block_distance + block_distance_from_turn
        elif self.kitchen_section.direction == EAST:
            kitchen_start_x += block_distance_from_turn
            kitchen_x += self.kitchen_section.block_distance + block_distance_from_turn
        elif self.kitchen_section.direction == SOUTH:
            kitchen_start_y -= block_distance_from_turn
            kitchen_y -= self.kitchen_section.block_distance + block_distance_from_turn
        elif self.kitchen_section.direction == WEST:
            kitchen_start_x -= block_distance_from_turn
            kitchen_x -= self.kitchen_section.block_distance + block_distance_from_turn

        if self.map_data.count((kitchen_x, kitchen_y)) == 0:
            self.temporary_potential_kitchen.append((kitchen_x, kitchen_y))

        #Loop inside function to be completed later!
        #self.add_temporary_potential_kitchen(kitchen_x, kitchen_start_x, kitchen_y, kitchen_start_y)

    # Appends all potential kitchen islands to temporary list
    def add_temporary_potential_kitchen(self, kitchen_x, kitchen_start_x, kitchen_y, kitchen_start_y):
        step_x = 1
        step_y = 1

        if kitchen_start_y == kitchen_y:
            if kitchen_start_x > kitchen_x:
                step_x = -1
            for x in range(kitchen_start_x, kitchen_x, step_x):
                if self.map_data.count((x, kitchen_y)) > 0:
                    self.temporary_potential_kitchen.append((x, kitchen_y))

        elif kitchen_start_x == kitchen_x:
            if kitchen_start_y > kitchen_y:
                step_y = -1
            for y in range(kitchen_start_y, kitchen_y, step_y):
                if self.map_data.count((kitchen_x, y)) > 0:
                    self.temporary_potential_kitchen.append((kitchen_x, y))
