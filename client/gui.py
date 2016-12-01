from tkinter import *
import outbound
import datetime


class GUI:
    WINDOW_X = 800
    WINDOW_Y = 600
    CANVAS_X = int(WINDOW_X * 0.6)
    CANVAS_Y = int(WINDOW_Y * 0.75)
    LIST_FRAME_X = int(WINDOW_X * 0.3)
    LIST_FRAME_Y = int(WINDOW_Y * 0.75)
    LIST_BOX_Y = int(LIST_FRAME_Y * 0.5)
    LIST_BOX_X = int(LIST_FRAME_X * 0.5)
    BT_FRAME_X = int(WINDOW_X)
    BT_FRAME_Y = int(WINDOW_Y * 0.2)
    
    MAX_LIST_ITEMS = 14
    

    def __init__(self):

        self.root = Tk()
        self.root.title("Kartoffel control")
        self.main_frame = Frame(self.root,width=self.WINDOW_X,height=self.WINDOW_Y)
        self.main_frame.grid()
        self.canvas = Canvas(self.main_frame,
                             width=GUI.CANVAS_X,
                             height=GUI.CANVAS_Y,bg="white")
        self.canvas.grid(column=0,row=0)
        
        self.list_frame = Frame(self.main_frame, width=self.LIST_FRAME_X, height=self.LIST_FRAME_Y)
        self.list_frame.grid(row=0,column=1)
        self.ir_list = Listbox(self.list_frame, height=14)
        self.ir_list.grid(row=0,column=1)
        self.ir_list_nr_items = 0

        self.laser_list = Listbox(self.list_frame, height=14)
        self.laser_list.grid(row=0,column=2)
        self.laser_list_nr_items = 0

        self.gyro_list = Listbox(self.list_frame, height=14)
        self.gyro_list.grid(row=2,column=1)
        self.gyro_list_nr_items = 0
 
        self.servo_list = Listbox(self.list_frame, height=14)
        self.servo_list.grid(row=2,column=2)
        self.servo_list_nr_items = 0
        
        self.bt_frame = Frame(self.main_frame,width=self.BT_FRAME_X,height=self.BT_FRAME_Y)
        self.bt_frame.grid(row=1)
        self.bt_forward = Button(self.bt_frame,text="Forward",command=outbound.bt_drive_forward)
        self.bt_forward.grid(row=0,column=1)
        self.bt_back = Button(self.bt_frame,text="Back",command=outbound.bt_drive_back)
        self.bt_back.grid(row=0,column=2)
        self.bt_right = Button(self.bt_frame,text="Right",command=outbound.bt_turn_right)
        self.bt_right.grid(row=0,column=3)
        self.bt_left = Button(self.bt_frame,text="Left",command=outbound.bt_turn_left)
        self.bt_left.grid(row=0,column=0)


    '''
    Values should be a list containing of [ir_left,ir_right,ir_left_back,
    ir_right_back,laser,gyro]
    '''

    def add_sensor_data(self, values):
        ir_values = str(values[2]) + ", " + str(values[0]) + ", " + str(values[1]) + ", " + str(values[3])
        
        self.ir_list.insert(0,ir_values)      
        if self.ir_list_nr_items >= self.MAX_LIST_ITEMS:  
            self.ir_list.delete(self.MAX_LIST_ITEMS)
        else:
            self.ir_list_nr_items += 1

        self.laser_list.insert(0, str(values[4]))
        if self.laser_list_nr_items >= self.MAX_LIST_ITEMS:
            self.laser_list.delete(self.MAX_LIST_ITEMS)
        else:
            self.laser_list_nr_items += 1  
        
        self.gyro_list.insert(0, str(values[5]))
        if self.gyro_list_nr_items >= self.MAX_LIST_ITEMS:
            self.gyro_list.delete(self.MAX_LIST_ITEMS)
        else:
            self.gyro_list_nr_items += 1

        print("IR values: ", str(values))

    '''
    Values should be a list containing of [left_speed,right_speed].
    '''

    def add_servo_data(self, values):
        if self.servo_list_nr_items >= self.MAX_LIST_ITEMS:
            for i in range(1,self.MAX_LIST_ITEMS):
                item = self.servo_list.get(i)
                self.servo_list.insert(i-1,item) 
        else:
            self.servo_list_nr_items += 1
        self.servo_list.insert(END, str(values[0]) + ', ' + str(values[1]))
        print("Servo data: ", str(values))

    def update_map(self, values):
        print("Map data: ", str(values))

