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
        self.map_data = [(0, 0)]
        self.current_x = 0
        self.current_y = 0
        self.kitchen_start_x = 0
        self.kitchen_start_y = 0
        self.kitchen_num_mapped = 0
        self.num_kitchen_turns = 0

        self.kitchen_mapping = {}
        self.invalid_kitchens = []

        self.num_ok_close = 0
        self.num_ok_far = 0

        EventBus.subscribe(CMD_TURN_STARTED, self.on_turning_started)
        EventBus.subscribe(CMD_TURN_FINISHED, self.on_turning_finished)

    def update(self):
        if self.state == STATE_MEASURING:
            distance = self.laser.get_data()
            self.current_section.add_distance_sample(distance)
            if self.mapping_state == MAPPING_STATE_FOLLOWING_OUTER_WALL:
                self.looking_for_kitchen_sections()
                self.remove_invalid_kitchen_sections()
            elif self.mapping_state == MAPPING_STATE_RETURNING_TO_ISLAND:
                self.check_if_returned_to_island()
            elif self.mapping_state == MAPPING_STATE_FOLLOWING_ISLAND:
                self.current_section.finish()
                temporary_x, temporary_y = self.transform_map_data(self.current_section, self.current_x, self.current_y, estimate=True)
                if temporary_x == self.kitchen_start_x and temporary_y == self.kitchen_start_y \
                        and self.kitchen_num_mapped > 3:
                    Navigator.force_left_turn = True

                    # Last island section is not properly stored because of a
                    # turn so we must store it here
                    self.store_ongoing_section()

                    self.mapping_state = MAPPING_STATE_RETURNING_TO_GARAGE

    def looking_for_kitchen_sections(self):
        if self.has_close_kitchen_left():
            self.add_kitchen_mapping(1, 0.5)

        if self.has_far_kitchen_left():
            self.add_kitchen_mapping(2, 0.25)

    def has_close_kitchen_left(self):
        match = self.ir.get_ir_left() > 10
        if match:
            self.num_ok_close += 1
        else:
            self.num_ok_close = 0

        if self.num_ok_close > 7:
            self.num_ok_close = 0
            return True
        else:
            return False

    def has_far_kitchen_left(self):
        match = 250 < self.ir.get_ir_left_back() < 650
        if match:
            self.num_ok_far += 1
        else:
            self.num_ok_far = 0

        if self.num_ok_far > 7:
            self.num_ok_far = 0
            return True
        else:
            return False

    def add_kitchen_mapping(self, displacement, offset):
        distance = self.current_section.estimate_block_distance(offset)
        cur_x, cur_y = self.transform_partial_map_data(distance, self.current_section.direction, self.current_x, self.current_y)
        key = self.get_left_block_coordinates(cur_x, cur_y, displacement)

        if key not in self.kitchen_mapping and key not in self.invalid_kitchens:
            print('Adding new mapping (' + str(key[0]) + ', ' + str(key[1]) + ') -> (' + str(cur_x) + ', ' + str(cur_y) + ')')
            self.kitchen_mapping[key] = (cur_x, cur_y)

    def remove_invalid_kitchen_sections(self):
        temporary_x, temporary_y = self.transform_map_data(self.current_section,
                                                           self.current_x,
                                                           self.current_y)
        key = self.get_right_block_coordinates(temporary_x, temporary_y, 1)
        popped = self.kitchen_mapping.pop(key, None)
        if popped is not None:
            print('Removed kitchen mapping for block (' + str(key[0]) + ', ' + str(key[1]) + ')')

        if key not in self.invalid_kitchens:
            print('Forbidding kitchen block at ' + str(key))
            self.invalid_kitchens.append(key)

    def check_if_returned_to_island(self):
        coordinates = self.transform_map_data(self.current_section,
                                              self.current_x,
                                              self.current_y,
                                              estimate=True)

        if coordinates in self.kitchen_mapping.values():
            print('Starting to map island!')

            self.mapping_state = MAPPING_STATE_FOLLOWING_ISLAND
            self.kitchen_num_mapped = 0
            self.num_kitchen_turns = 0
            key1 = self.transform_partial_map_data(1, self.current_section.direction, coordinates[0], coordinates[1])
            key2 = self.transform_partial_map_data(2, self.current_section.direction, coordinates[0], coordinates[1])
            if key1 not in self.kitchen_mapping and key2 not in self.kitchen_mapping:
                Navigator.force_left_turn = True
            else:
                Navigator.right_turn_enabled = False

    def save_current_section(self):
        if self.mapping_state == MAPPING_STATE_FOLLOWING_OUTER_WALL:
            self.process_finished_section()

            print('---- SECTION SAVED ----')
            print('  direction: ' + str(self.current_section.direction))
            print('  distance: ' + str(self.current_section.block_distance))
            print('  coordinates: ' + str(self.current_x) + ", " + str(self.current_y))
            print('  kitchen mappings: \n' + self.get_kitchen_debug_data())
            print('-----------------------')
        elif self.mapping_state == MAPPING_STATE_FOLLOWING_ISLAND:
            self.process_finished_section()

            print('---- ISLAND ROUNDED ----')
            print('  direction: ' + str(self.current_section.direction))
            print('  distance: ' + str(self.current_section.block_distance))
            print('  coordinates: ' + str(self.current_x) + ", " + str(self.current_y))
            print('-----------------------')

            self.kitchen_num_mapped += 1
            self.num_kitchen_turns += 1
        else:
            self.process_finished_section(store_data=False)

            print('---- SECTION TRAVELLED ----')
            print('  direction: ' + str(self.current_section.direction))
            print('  distance: ' + str(self.current_section.block_distance))
            print('  coordinates: ' + str(self.current_x) + ", " + str(self.current_y))
            print('-----------------------')

    def get_kitchen_debug_data(self):
        data = []
        for k, v in self.kitchen_mapping.items():
            data.append('    ' + str(k) + ' -> ' + str(v))

        return '\n'.join(data)

    def begin_next_section(self, is_right_turn):
        if is_right_turn:
            self.current_section = self.current_section.for_right_turn()
        else:
            self.current_section = self.current_section.for_left_turn()

    def on_turning_started(self):
        if self.mapping_state == MAPPING_STATE_RETURNING_TO_GARAGE:
            if self.has_returned_to_start(include_direction=False):
                self.state = STATE_FINISHED
                self.navigator.set_mode(Navigator.MANUAL)
                print(self.map_data)
        else:
            self.state = STATE_WAITING

        self.save_current_section()

    def on_turning_finished(self, is_right_turn):
        self.begin_next_section(is_right_turn)
        if self.has_returned_to_start() or self.mapping_state == MAPPING_STATE_RETURNING_TO_ISLAND:
            self.mapping_state = MAPPING_STATE_RETURNING_TO_ISLAND

        if self.mapping_state == MAPPING_STATE_FOLLOWING_ISLAND and self.num_kitchen_turns == 2:
            self.kitchen_start_x = self.current_x
            self.kitchen_start_y = self.current_y

        self.state = STATE_MEASURING

    def has_returned_to_start(self, include_direction=True):

        if self.current_x == 0 and self.current_y == 0 and len(self.map_data) > 0:
            return not include_direction or self.current_section.direction == NORTH
        else:
            return False

    def transform_map_data(self, section, current_x, current_y, estimate=False):
        if estimate:
            distance = section.estimate_block_distance()
        else:
            section.finish()
            distance = section.block_distance

        return self.transform_partial_map_data(distance, section.direction, current_x, current_y)

    def transform_partial_map_data(self, distance, direction, current_x, current_y):
        if direction == NORTH:
            current_y += distance
        elif direction == EAST:
            current_x += distance
        elif direction == SOUTH:
            current_y -= distance
        elif direction == WEST:
            current_x -= distance
        return current_x, current_y

    def store_ongoing_section(self):
        self.current_section.finish()

        distance = self.current_section.block_distance
        direction = self.current_section.direction

        for i in range(1, distance + 1):
            pos_x, pos_y = self.transform_partial_map_data(i, direction, self.current_x, self.current_y)
            self.map_data.append((pos_x, pos_y))

    def process_finished_section(self, store_data=True):
        self.current_section.finish(debug_limits=True)

        if store_data:
            distance = self.current_section.block_distance
            direction = self.current_section.direction

            for i in range(1, distance + 1):
                coordinates = self.transform_partial_map_data(i, direction, self.current_x, self.current_y)
                self.map_data.append(coordinates)
                self.kitchen_mapping.pop(coordinates, None)
                if coordinates not in self.invalid_kitchens:
                    self.invalid_kitchens.append(coordinates)

            self.saved_sections.append(self.current_section)

        # Could be optimized to use last pos_x, pos_y instead
        self.current_x, self.current_y = self.transform_map_data(self.current_section, self.current_x, self.current_y)

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

    def get_left_block_coordinates(self, x, y, displacement):
        if self.current_section.direction == NORTH:
            x -= displacement
        elif self.current_section.direction == EAST:
            y += displacement
        elif self.current_section.direction == SOUTH:
            x += displacement
        elif self.current_section.direction == WEST:
            y -= displacement

        return x, y

    def get_right_block_coordinates(self, x, y, displacement):
        return self.get_left_block_coordinates(x, y, -displacement)
