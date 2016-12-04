from datetime import datetime

import math
import os

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

BLOCK_LENGTH_MM = 400


class Section:
    FILE_NUM = 0

    def __init__(self, direction):
        self.direction = direction
        self.measurements = []
        self.block_distance = None

        if Section.FILE_NUM == 1:
            open("debug.txt", "w").close()
            os.remove("debug.txt")
            self.file = open("debug.txt", "w")
            self.file.write("Start distance; Start-finish distance; Estimated start distance; "
                            "Non-manipulated Block distance; Manipulated block distance \n")
            self.file.flush()
            self.file.close()
            Section.FILE_NUM = 1


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

        first_measurement = self.measurements[0]
        last_measurement = self.measurements[-1]

        start_time = first_measurement[1]

        finish_distance = last_measurement[0]
        finish_time = last_measurement[1]

        ratio_sum = 0
        for measurement in self.measurements:
            raw_distance = measurement[0]
            measurement_time = measurement[1]

            distance_diff = raw_distance - finish_distance
            time_diff = finish_time - measurement_time
            time_diff_seconds = time_diff.total_seconds()
            if time_diff_seconds == 0:
                # Avoid division by zero, skip last measurement
                continue

            ratio = distance_diff / time_diff_seconds
            ratio_sum += ratio

        average_ratio = ratio_sum / len(self.measurements)
        total_measure_time_seconds = (finish_time - start_time).total_seconds()
        estimated_start_distance = average_ratio * total_measure_time_seconds
        print("Estimated start distance: " + str(estimated_start_distance))
        print("Non rounded blockdistance: " + str(estimated_start_distance/BLOCK_LENGTH_MM))
        self.block_distance = round(
            (estimated_start_distance / BLOCK_LENGTH_MM)
        )
        self.file = open("debug.txt", "a")
        self.file.write(str(first_measurement[0]) + ";" + str(first_measurement[0] - finish_distance) + ";"
                        + str(estimated_start_distance) + ";" + str(estimated_start_distance / BLOCK_LENGTH_MM) + ";"
                        + str(self.block_distance) + "\n")
        self.file.flush()
        self.file.close()

    def for_right_turn(self):
        return Section((self.direction + 1) % 4)

    def for_left_turn(self):
        return Section((self.direction - 1) % 4)
