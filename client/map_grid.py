
class MapGrid:
    
    MAX_MAP_SIZE = 6000   # relative size (mm)
    CELL_SIZE = 400       # relative size (mm)
    NR_ROWS = MAX_MAP_SIZE // CELL_SIZE
    NR_COLS = NR_ROWS

    def __init__(self):
        # List of coordinates of all corners on the map,
        # listed in the order of discovery
        self.map_data = []
        self.new_map_data = []              # The latest map data received
        self.new_map_data_actual_coords = []
        self.start_position = (0, 0)
        # Offset calculated from given coordinates to match coordinates on map grid
        self.x_offset = 0
        self.y_offset = 0

    def update_map(self, data, canvas):
        self._update_map_data(data)
        self._calc_actual_coords(canvas)
        self._draw_lines(canvas)

    '''
    Expects data to be a list containing ALL map data coordinates.
    '''
    def _update_map_data(self, data):
        #nr_new_items = len(data) - len(self.map_data)
        #self.new_map_data = data[:nr_new_items]
        #self.map_data = data
        self.new_map_data = data

    '''
    Appends internal list of new corners with actual coordinates corresponding to
    size of map in pixels.
    '''
    def _calc_actual_coords(self, canvas):
        for corner in self.new_map_data:
            # Match coordinates to grid
            x = corner[0]
            mod_x = x % self.CELL_SIZE
            if mod_x < (self.CELL_SIZE / 2):
                x = (x // self.CELL_SIZE) * self.CELL_SIZE
            else:
                x = ((x // self.CELL_SIZE) + 1) * self.CELL_SIZE
            y = corner[1]
            mod_y = y % self.CELL_SIZE
            if mod_y < (self.CELL_SIZE / 2):
                y = (y // self.CELL_SIZE) * self.CELL_SIZE
            else:
                y = ((y // self.CELL_SIZE) + 1) * self.CELL_SIZE

            actual_x = (canvas.winfo_width() * x) // (self.CELL_SIZE * self.NR_COLS)
            actual_y = (canvas.winfo_height() * y) // (self.CELL_SIZE * self.NR_ROWS)
            self.new_map_data_actual_coords.append((actual_x, actual_y))
    '''
    Draw lines between corners. Replaces map data with actual coordinates with only the last
    visited corner.
    '''
    def _draw_lines(self, canvas):
        corners = self.new_map_data_actual_coords
        for i in range(0, len(corners)-1):
            canvas.create_line(corners[i][0], corners[i][1], corners[i+1][0], corners[i+1][1], fill="black")
            print("Drawing line between: ", corners[i][0], ",", corners[i][1], "and", corners[i+1][0], ",",
                  corners[i+1][1])
        # Replace the list with only the last visited corner
        print("Storing end corner: ", corners[len(corners)-1][0], ", ", corners[len(corners)-1][1])
        self.new_map_data_actual_coords = [corners[len(corners)-1]]
