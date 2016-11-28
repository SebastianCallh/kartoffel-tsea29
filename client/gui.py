import tkinter

from eventbus import EventBus

class GUI:

    CANVAS_X_SIZE = 500
    CANVAS_Y_SIZE = 500
    UPDATE_INTERVALL = 0.25
    
    root = None
    canvas = None
    
    def __init__(self):
        global root,canvas
        root = Tk()
        canvas = Canvas(root,CANVAS_X_SIZE,CANVAS_Y_SIZE)
        canvas.pack()
    
    def start():
        canvas.after(UPDATE_INTERVALL, update)
        root.mainloop()
        
    def update():
        EventBus.receive()
        
    def add_sensor_data(args*):
        pass
        
    def add_servo_data(args*):
        pass
        
    def update_map(args*):
        pass
    


