gui = None

def printIP(task):
    global gui
    gui.printIP()
    
def add_sensor_data(task):
    global gui
    gui.add_sensor_data(task.data)
    
def add_servo_data(task):
    global gui
    gui.add_servo_data(task.data)
    
def update_map(task):
    global gui
    gui.update_map(task.data)
