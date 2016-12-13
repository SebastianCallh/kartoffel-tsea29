from datetime import datetime
from math import floor


NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

BLOCK_LENGTH_MM = 400


class Section:
    UNREASONABLE_DIFF = 1000
    VERY_REASONABLE_DIFF = 100

    def __init__(self, direction):
        self.direction = direction
        self.measurements = []
        self.block_distance = None
        self.measured_distances = 0
        self.pending_unreasonable_value = None

    def add_distance_sample(self, distance):
        if 50 < distance < 6000:
            if len(self.measurements) > 0:
                last_measurement = self.measurements[-1][0]
                if abs(last_measurement - distance) > self.UNREASONABLE_DIFF:
                    if self.pending_unreasonable_value is not None:
                        if abs(self.pending_unreasonable_value - distance) < self.VERY_REASONABLE_DIFF:
                            self.measurements.append((self.pending_unreasonable_value, datetime.now()))
                            self.measurements.append((distance, datetime.now()))
                            self.pending_unreasonable_value = None
                            return

                    self.pending_unreasonable_value = distance
                    return

            self.pending_unreasonable_value = None
            self.measured_distances += 1

            if self.measured_distances >= 7:
                self.measurements.append((distance, datetime.now()))

    def finish(self, debug_limits=False):
        # If we're somehow detecting the next turn for a dead end corner before
        # any measurements have been received our normal algorithm won't work.
        # Handle this by explicitly setting the distance to zero.
        if len(self.measurements) == 0:
            self.block_distance = 0
            return

        # Takes the difference between max measurement and min measurement and divide by block length.
        self.block_distance = round((self.get_max(debug_limits) - self.get_min(debug_limits)) / BLOCK_LENGTH_MM)

    def estimate_block_distance(self, offset=0.25):
        if len(self.measurements) == 0:
            return 0

        # Takes the difference between max measurement and min measurement and divide by block length.
        return floor((self.get_max() - self.get_min()) / BLOCK_LENGTH_MM + offset)

    def for_right_turn(self):
        return Section((self.direction + 1) % 4)

    def for_left_turn(self):
        return Section((self.direction - 1) % 4)

    def get_max(self, debug_limits=False):
        if len(self.measurements) == 0:
            return 0

        value = max(self.measurements, key=lambda x: x[0])[0]
        if debug_limits:
            print('Max', value)

        return value

    def get_min(self, debug_limits=False):
        if len(self.measurements) == 0:
            return 0

        value = min(self.measurements, key=lambda x: x[0])[0]
        if debug_limits:
            print('Min', value)

        return value