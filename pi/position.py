from eventbus import EventBus
from laser import Laser
from protocol import CMD_TURN_STARTED, CMD_TURN_FINISHED
from section import Section, NORTH, EAST, SOUTH, WEST
from threading import Thread

STATE_MEASURING = 0
STATE_WAITING = 1


class Position:
    def __init__(self, laser):
        self.laser = laser
        self.state = STATE_MEASURING
        self.current_section = Section(NORTH)
        self.saved_sections = []
        self.map_data = []
        self.current_x = 0
        self.current_y = 0

        EventBus.subscribe(CMD_TURN_STARTED, self.on_turning_started)
        EventBus.subscribe(CMD_TURN_FINISHED, self.on_turning_finished)

    def update(self):
        if self.state == STATE_MEASURING:
            distance = self.laser.get_data()
            self.current_section.add_distance_sample(distance)

    def save_current_section(self):
        self.current_section.finish()

        self.saved_sections.append(self.current_section)
        self.map_data.append(self.transform_map_data(self.current_section))
        print('---- SECTION SAVED ----')
        print('  direction: ' + str(self.current_section.direction))
        print('  distance: ' + str(self.current_section.block_distance))
        print('  coordinates: ' + str(self.current_x) + ", " + str(self.current_y))
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
        #self.save_current_section()

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
