from eventbus import EventBus
from laser import Laser
from protocol import CMD_TURN_STARTED, CMD_TURN_FINISHED
from section import Section, NORTH
from threading import Thread

STATE_MEASURING = 0
STATE_WAITING = 1


class Position:
    def __init__(self, laser):
        self.laser = laser
        self.state = STATE_MEASURING
        self.current_section = Section(NORTH)
        self.saved_sections = []

        EventBus.subscribe(CMD_TURN_STARTED, self.on_turning_started)
        EventBus.subscribe(CMD_TURN_FINISHED, self.on_turning_finished)

    def update(self):
        if self.state == STATE_MEASURING:
            distance = self.laser.get_data()
            self.current_section.add_distance_sample(distance)

    def save_current_section(self):
        self.current_section.finish()

        print('---- SECTION SAVED ----')
        print('  direction: ' + str(self.current_section.direction))
        print('  distance: ' + str(self.current_section.block_distance))
        print('-----------------------')

        self.saved_sections.append(self.current_section)

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

    '''
    Returns a list of tuples with coordinates of all the corners
    '''
    def get_map_data(self):
        return [(10, 20), (30, 10)]