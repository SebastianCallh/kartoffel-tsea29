from eventbus import EventBus
from laser import Laser
from navigator import Navigator
from protocol import CMD_TURN_STARTED, CMD_TURN_FINISHED
from section import Section, NORTH, EAST, SOUTH, WEST, BLOCK_LENGTH_MM
from threading import Thread

STATE_MEASURING = 0
STATE_WAITING = 1
STATE_FINISHED = 2

MAPPING_STATE_FOLLOWING_OUTER_WALL = 0
MAPPING_STATE_RETURNING_TO_ISLAND = 1
MAPPING_STATE_FOLLOWING_ISLAND = 2
MAPPING_STATE_RETURNING_TO_GARAGE = 3


class Position:
    def __init__(self, laser, ir, navigator):
        self.laser = laser
        self.ir = ir
        self.navigator = navigator
        self.state = STATE_MEASURING
        self.mapping_state = MAPPING_STATE_FOLLOWING_OUTER_WALL
        self.current_section = Section(NORTH)
        self.saved_sections = []
        self.map_data = []
        self.current_x = 0
        self.current_y = 0
        self.kitchen_start_x = 0
        self.kitchen_start_y = 0

        self.kitchen_section = Section(NORTH)
        self.looking_for_kitchen = False
        self.kitchen_block_displacement = 0
        self.potential_kitchen = []
        self.temporary_potential_kitchen = []
        self.long_measurements_count = 0

        EventBus.subscribe(CMD_TURN_STARTED, self.on_turning_started)
        EventBus.subscribe(CMD_TURN_FINISHED, self.on_turning_finished)

    def update(self):
        if self.state == STATE_MEASURING:
            distance = self.laser.get_data()
            self.current_section.add_distance_sample(distance)
            if self.mapping_state == MAPPING_STATE_FOLLOWING_OUTER_WALL:
                self.looking_for_kitchen_sections(distance)
            elif self.mapping_state == MAPPING_STATE_RETURNING_TO_ISLAND:
                self.current_section.finish()
                temporary_x, temporary_y = self.transform_map_data(self.current_section, self.current_x, self.current_y)
                if self.potential_kitchen.count((temporary_x, temporary_y)) > 0:
                    self.mapping_state = MAPPING_STATE_FOLLOWING_ISLAND
                    self.kitchen_start_x = temporary_x
                    self.kitchen_start_y = temporary_y
                    Navigator.force_left_turn = True
            elif self.mapping_state == MAPPING_STATE_FOLLOWING_ISLAND:
                temporary_x, temporary_y = self.transform_map_data(self.current_section, self.current_x, self.current_y)
                if temporary_x == self.kitchen_start_x and temporary_y == self.kitchen_start_y:
                    Navigator.force_left_turn = True
                    self.mapping_state = MAPPING_STATE_RETURNING_TO_GARAGE



    def looking_for_kitchen_sections(self, distance):
        # If im looking for a kitchen, add sample.
        if self.looking_for_kitchen:
            self.kitchen_section.add_distance_sample(distance)

        # Checks if a kitchen island may be present and start calculating sections for it.
        if self.ir.get_ir_left() > 10 and not self.looking_for_kitchen:
            print("start for kitchen")
            self.looking_for_kitchen = True
            self.kitchen_section = Section(self.current_section.direction)
            self.temporary_potential_kitchen = []
            self.kitchen_section.add_distance_sample(distance)
            self.kitchen_block_displacement = 0

        elif 250 < self.ir.get_ir_left_back() < 650 and not self.looking_for_kitchen:
            # Lets the first 10 measurements pass to skip noise.
            if self.long_measurements_count >= 5:
                self.long_measurements_count = 0
                print("start for kitchen long, distance: " + str(self.ir.get_ir_left_back()))
                self.looking_for_kitchen = True
                self.kitchen_section = Section(self.current_section.direction)
                self.temporary_potential_kitchen = []
                self.kitchen_section.add_distance_sample(distance)
                self.kitchen_block_displacement = 1
            else:
                self.long_measurements_count += 1

        elif not self.looking_for_kitchen:
            self.long_measurements_count = 0

        elif ((self.ir.get_ir_left() == -1 and self.kitchen_block_displacement == 0) or
                  (0 < self.ir.get_ir_left_back() < 250 and self.kitchen_block_displacement == 1)) and \
                self.looking_for_kitchen:

            self.kitchen_section.finish()
            self.calculate_kitchen_coordinates()
            self.looking_for_kitchen = False
            self.kitchen_section = Section(self.current_section.direction)

    def save_current_section(self):
        self.current_section.finish()
        self.current_x, self.current_y = self.transform_map_data(self.current_section, self.current_x, self.current_y)
        if self.mapping_state == MAPPING_STATE_FOLLOWING_OUTER_WALL:
            self.saved_sections.append(self.current_section)
            self.map_data.append((self.current_x, self.current_y))

            print("Primary temporary kitchens: " + str(self.temporary_potential_kitchen))

            # Removes potential kitchens if already passed - !!not TRUE!!
            # TODO: Rethink about this if statement.
            if self.potential_kitchen.count((self.current_x, self.current_y)) > 0:
                self.potential_kitchen.remove((self.current_x, self.current_y))

            # Adds all new potential kitchens that does not exist in map.
            for section in self.temporary_potential_kitchen:
                if self.map_data.count((section[0], section[1])) == 0:
                    self.potential_kitchen.append(section)

            print('---- SECTION SAVED ----')
            print('  direction: ' + str(self.current_section.direction))
            print('  distance: ' + str(self.current_section.block_distance))
            print('  coordinates: ' + str(self.current_x) + ", " + str(self.current_y))
            print('  potential kitchens: ' + str(self.potential_kitchen))
            print('-----------------------')
        else:
            print('---- SECTION TRAVELLED ----')
            print('  direction: ' + str(self.current_section.direction))
            print('  distance: ' + str(self.current_section.block_distance))
            print('  coordinates: ' + str(self.current_x) + ", " + str(self.current_y))
            print('-----------------------')

    def begin_next_section(self, is_right_turn):
        if is_right_turn:
            self.current_section = self.current_section.for_right_turn()
            self.kitchen_section = self.kitchen_section.for_right_turn()
        else:
            self.current_section = self.current_section.for_left_turn()
            self.kitchen_section = self.kitchen_section.for_left_turn()

    def on_turning_started(self):
        if self.mapping_state == MAPPING_STATE_RETURNING_TO_GARAGE:
            if self.has_returned_to_start(include_direction=False):
                self.state = STATE_FINISHED
                self.navigator.set_mode(Navigator.MANUAL)
        else:
            self.state = STATE_WAITING
            if self.looking_for_kitchen:
                self.kitchen_section.finish()
                self.calculate_kitchen_coordinates()
                self.looking_for_kitchen = False
        self.save_current_section()

    def on_turning_finished(self, is_right_turn):
        self.begin_next_section(is_right_turn)
        if self.has_returned_to_start() or self.mapping_state == MAPPING_STATE_RETURNING_TO_ISLAND:
            self.mapping_state = MAPPING_STATE_RETURNING_TO_ISLAND

        self.state = STATE_MEASURING

    def has_returned_to_start(self, include_direction=True):

        if self.current_x == 0 and self.current_y == 0 and len(self.map_data) > 0:
            return not include_direction or self.current_section.direction == NORTH
        else:
            return False

    def transform_map_data(self, section, current_x, current_y):
        if section.direction == NORTH:
            current_y += section.block_distance
        elif section.direction == EAST:
            current_x += section.block_distance
        elif section.direction == SOUTH:
            current_y -= section.block_distance
        elif section.direction == WEST:
            current_x -= section.block_distance
        return current_x, current_y

    '''
    Returns a list of tuples with coordinates of grids visited
    '''
    def get_map_data(self):
        return [self.map_data]

    '''
    Returns the robots last know x,y coordinates
    '''
    def get_current_position(self):
        return self.current_x, self.current_y

    def calculate_kitchen_coordinates(self):
        if self.kitchen_section.block_distance > 0:
            block_distance_from_turn = round((self.current_section.get_max() - self.kitchen_section.get_max()) /
                                             BLOCK_LENGTH_MM)
            print("Section max: " + str(self.current_section.get_max()) +
                  ", Kitchen max: " + str(self.kitchen_section.get_max()))

            print("Kitchen block distance from turn: " + str(block_distance_from_turn))

            kitchen_x = self.current_x
            kitchen_y = self.current_y

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
            kitchen_start_x = kitchen_x
            kitchen_start_y = kitchen_y

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

            self.temporary_potential_kitchen.append((kitchen_x, kitchen_y))
            print("Kitchen block distance: " + str(self.kitchen_section.block_distance))
            print("Kitchen start coordinates: " + str(kitchen_start_x) + ", " + str(kitchen_start_y))
            print("Kitchen end coordinates: " + str(kitchen_x) + ", " + str(kitchen_y))

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
