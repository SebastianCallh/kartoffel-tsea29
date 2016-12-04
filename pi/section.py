from datetime import datetime


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

BLOCK_LENGTH_MM = 400


class Section:

    def __init__(self, direction):
        self.direction = direction
        self.measurements = []
        self.block_distance = None


    def add_distance_sample(self, distance):
        # TODO: Verify distance validity by checking if the delta distance is
        # reasonable.
        if distance > 50:
            self.measurements.append((distance, datetime.now()))

    def finish(self):
        # If we're somehow detecting the next turn for a dead end corner before
        # any measurements have been received our normal algorithm won't work.
        # Handle this by explicitly setting the distance to zero.
        if len(self.measurements) == 0:
            self.block_distance = 0
            return

        # Takes the difference between max measurement and min measurement and divide by block length.
        self.block_distance = round(
            (max(self.measurements, key=lambda x: x[0])[0] -
             min(self.measurements, key=lambda x: x[0])[0]) /
            BLOCK_LENGTH_MM)

    def for_right_turn(self):
        return Section((self.direction + 1) % 4)

    def for_left_turn(self):
        return Section((self.direction - 1) % 4)
