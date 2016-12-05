
class MapGrid:
    
    MAX_MAP_SIZE = 15 * 2   # 1 cell is 40x40 cm, 28 x 28 cells in map
    # CELL_SIZE = 1
    NR_ROWS = MAX_MAP_SIZE
    NR_COLS = NR_ROWS
    OFFSET = 15

    def __init__(self):
        # List of coordinates of all corners on the map,
        # listed in the order of discovery
        self.raw_map_data = []
        self.actual_map_data = []
        self.new_raw_map_data = []              # The latest map data received
        self.new_actual_map_data = []
        self.start_position = (self.OFFSET, self.OFFSET)
        # Offset calculated from given coordinates to match coordinates on map grid

    def update_map(self, data, canvas):
        self._update_map_data(data)
        self.new_actual_map_data = []
        for cycle in data:
            self._calc_actual_coords(canvas, cycle)
            self._draw_lines(canvas)

    '''
    Expects data to be a list containing ALL map data coordinates.
    '''
    def _update_map_data(self, data):
        #nr_new_items = len(data) - len(self.raw_map_data)
        #self.new_raw_map_data = data[:nr_new_items]
        #self.raw_map_data = data
        self.new_raw_map_data = data

    '''
    Appends internal list of corners with actual coordinates corresponding to
    size of map in pixels.
    '''
    def _calc_actual_coords(self, canvas, cycle):
        for corner in cycle:
            # Match coordinates to grid
            x = corner[0]
            x += self.OFFSET

            y = corner[1]
            y += self.OFFSET

            # Convert raw coordinates to actual coordinates corresponding to canvas pixels
            #actual_x = (canvas.winfo_width() * x) // (self.CELL_SIZE * self.NR_COLS)
            actual_x = canvas.winfo_width() * x // self.NR_COLS
            #actual_y = (canvas.winfo_height() * y) // (self.CELL_SIZE * self.NR_ROWS)
            actual_y = canvas.winfo_height() * y // self.NR_ROWS
            self.new_actual_map_data.append((actual_x, actual_y))

    '''
    Draw lines between corners. Replaces map data with actual coordinates with only the last
    visited corner.
    '''
    def _draw_lines(self, canvas):
        corners = self.new_actual_map_data
        for i in range(0, len(corners)-1):
            canvas.create_line(corners[i][0], corners[i][1], corners[i+1][0], corners[i+1][1], fill="black")
            self.actual_map_data.append(corners[i])
            print("Drawing line between: ", corners[i][0], ",", corners[i][1], "and", corners[i+1][0], ",", corners[i+1][1])
            self.actual_map_data.append(corners[i])

        # Replace the list with only the last visited corner
        print("Storing end corner: ", corners[len(corners)-1][0], ", ", corners[len(corners)-1][1])
        last_corner = corners[len(corners)-1]
        self.new_actual_map_data = [last_corner]

