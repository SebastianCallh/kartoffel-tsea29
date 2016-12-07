class MapGrid:
    MAX_MAP_SIZE = 15 * 2  # 1 cell is 40x40 cm, 28 x 28 cells in map
    NR_ROWS = MAX_MAP_SIZE
    NR_COLS = NR_ROWS
    OFFSET = 15

    def __init__(self):
        # List of coordinates of all corners on the map,
        # listed in the order of discovery
        self.raw_map_data = []
        self.actual_map_data = []
        self.new_raw_map_data = []  # The latest map data received
        self.new_actual_map_data = []
        self.start_position = (self.OFFSET, self.OFFSET)
        # Offset calculated from given coordinates to match coordinates on map grid

    def update_map(self, data, canvas):
        self._update_map_data(data)
        self.new_actual_map_data = []
        self._calc_actual_coords(canvas, data)
        self._draw_blocks(canvas)

    def draw_grid(self, canvas):
        size = canvas.winfo_width() / self.NR_ROWS
        print("size =", size)
        for row in range(0, self.NR_ROWS):
            canvas.create_line(0, row * size, canvas.winfo_width(), row * size, fill="#FFFFFF")
            canvas.create_line(row * size, 0, row * size, canvas.winfo_width(), fill="#FFFFFF")

    '''
    Expects data to be a list containing ALL map data coordinates.
    '''

    def _update_map_data(self, data):
        nr_new_items = len(data) - len(self.raw_map_data)
        self.new_raw_map_data = data[:nr_new_items]
        self.raw_map_data = data
        self.new_raw_map_data = data

    '''
    Appends internal list of corners with actual coordinates corresponding to
    size of map in pixels.
    '''

    def _calc_actual_coords(self, canvas, visited):
        print("visited =", visited)
        for block in visited:
            # Match coordinates to grid
            print("block = ", block)
            x = block[0][0]
            y = block[0][1]
            x += self.OFFSET
            y += self.OFFSET

            # Convert raw coordinates to actual coordinates corresponding to canvas pixels
            actual_x = (canvas.winfo_width() * x) / self.NR_COLS
            actual_y = (canvas.winfo_height() * y) / self.NR_ROWS
            self.new_actual_map_data.append((actual_x, actual_y))

    '''
    Draw lines between corners. Replaces map data with actual coordinates with only the last
    visited corner.
    '''

    def _draw_blocks(self, canvas):
        block_size = canvas.winfo_height() / self.NR_ROWS

        visited = self.new_actual_map_data
        for block in visited:
            canvas.create_rectangle(block[0], block[1], block[0] + block_size, block[1] + block_size,
                                    fill="#FFFFFF", outline="white")
            self.actual_map_data.append(block)
