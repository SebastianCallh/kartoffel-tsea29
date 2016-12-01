from tkinter import *
import outbound
import datetime


class GUI:
    WINDOW_X = 800
    WINDOW_Y = 600
    CANVAS_X = WINDOW_X * 0.6
    CANVAS_Y = WINDOW_Y * 0.75
    LIST_FRAME_X = WINDOW_X * 0.75
    LIST_FRAME_Y = WINDOW_Y * 0.3
    BT_FRAME_X = WINDOW_X
    BT_FRAME_Y = WINDOW_Y * 0.2
    

    MAX_LIST_ITEMS = 10

    UPDATE_INTERVAL = 250  # milliseconds

    def __init__(self):

        self.root = Tk()
        self.main_frame = Frame(self.root,width=self.WINDOW_X,height=self.WINDOW_Y)
        self.main_frame.grid()
        self.canvas = Canvas(self.main_frame,
                             width=GUI.CANVAS_X,
                             height=GUI.CANVAS_Y,bg="red")
        self.canvas.grid(column=0,row=0)
        
        self.list_frame = Frame(self.main_frame, width=self.LIST_FRAME_X, height=self.LIST_FRAME_Y)
        self.list_frame.grid(row=0,column=1)
        self.ir_list = Listbox(self.list_frame)
        self.ir_list.grid(row=0,column=1)
        self.ir_list_nr_items = 0

        self.laser_list = Listbox(self.list_frame)
        self.laser_list.grid(row=0,column=2)
        self.lasert_list_nr_items = 0

        self.gyro_list = Listbox(self.list_frame)
        self.gyro_list.grid(row=2,column=1)
        self.gyro_list_nr_items = 0
 
        self.servo_list = Listbox(self.list_frame)
        self.servo_list.grid(row=2,column=2)
        self.servo_list_nr_items = 0
        
        self.bt_frame = Frame(self.main_frame,width=self.BT_FRAME_X,height=self.BT_FRAME_Y)
        self.bt_frame.grid(row=1)
        self.bt_forward = Button(self.bt_frame,text="Forward",command=outbound.bt_drive_forward)
        self.bt_forward.grid(row=0,column=0)
        self.bt_back = Button(self.bt_frame,text="Back",command=outbound.bt_drive_back)
        self.bt_back.grid(row=0,column=1)


    '''
    Values should be a list containing of [ir_left,ir_right,ir_left_back,
    ir_right_back,laser,gyro]
    '''

    def add_sensor_data(self, values):
        '''ir_values = str(values[2]) + ", " + str(values[0]) + ", " + str(values[1]) + ", " + str(values[3])

        ir_values = str(values)
        self.ir_list.insert(END, ir_values)
        self.laser_list.insert(END, str(values[4]))
        self.gyro_list.insert(END, str(values[5]))'''
        print("IR values: ", str(values))

    '''
    Values should be a list containing of [left_speed,right_speed].
    '''

    def add_servo_data(self, values):
        #self.servo_list.insert(str(values[0]), str(values[1]))
        print("Servo data: ", str(values))

    def update_map(self, values):
        pass

