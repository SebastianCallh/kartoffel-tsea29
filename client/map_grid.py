
class map_grid():
    
    MAX_MAP_SIZE = 6000   # mm
    CELL_SIZE = 400       # mm
    NR_ROWS = MAX_MAP_SIZE // CELL_SIZE
    NR_COLS = NR_ROWS
    
    def __init__():
        self.map_data = []       # List of coordinates of all corners on the map,
                                 # listed in the order of discovery
        self.new_map_data = []   # The latest map data recieved
        self.start_position = 
