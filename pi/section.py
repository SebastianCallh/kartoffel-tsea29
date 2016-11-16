NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3


class Section:
    def __init__(self, direction):
        self.direction = direction

    def store_distance(self):
        pass

    def finish(self):
        pass

    def for_right_turn(self):
        return Section((self.direction + 1) % 4)

    def for_left_turn(self):
        return Section((self.direction - 1) % 4)
