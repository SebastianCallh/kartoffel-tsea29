from tkinter import *
import outbound
import datetime


class GUI:
    CANVAS_X_SIZE = 500
    CANVAS_Y_SIZE = 500

    MAX_LIST_ITEMS = 10

    UPDATE_INTERVAL = 0.25  # seconds
    DATA_REQUEST_INTERVAL = 1  # seconds

    def __init__(self, queue_handler):
        self.last_data_request_time = datetime.datetime.now()

        self.root = Tk()
        self.canvas = Canvas(self.root,
                             width=GUI.CANVAS_X_SIZE,
                             height=GUI.CANVAS_Y_SIZE)
        self.canvas.pack()
        self.ir_list = Listbox(self.root)
        self.ir_list_nr_items = 0
        self.ir_list.pack()
        self.laser_list = Listbox(self.root)
        self.laser_list.pack()
        self.gyro_list = Listbox(self.root)
        self.gyro_list.pack()
        self.servo_list = Listbox(self.root)
        self.servo_list.pack()
        self.queue_handler = queue_handler

    '''
    Values should be a list containing of [ir_left,ir_right,ir_left_back,
    ir_right_back,laser,gyro]
    '''

    def add_sensor_data(self, values):
        ir_values = str(values[2]) + "," + str(values[0]) + "," + str(values[1]) + "," + str(values[3])

        self.ir_list.insert(END, ir_values)
        self.laser_list.insert(END, str(values[4]))
        self.gyro_list.insert(END, str(values[5]))

    '''
    Values should be a list containing of [left_speed,right_speed].
    '''

    def add_servo_data(self, values):
        self.servo_list.insert(str(values[0]), str(values[1]))

    def update_map(self, values):
        pass

    def _request_data(self):
        outbound.bt_request_sensor_data()
        outbound.bt_request_servo_data()
        outbound.bt_request_map_data()

    def _update(self):
        self.queue_handler.eventbus.receive()
        if (datetime.datetime.now() - self.last_data_request_time) > datetime.timedelta(
                seconds=GUI.DATA_REQUEST_INTERVAL):
            self._request_data()
        self.canvas.after(GUI.UPDATE_INTERVAL, self._update)

    def start(self):
        self.canvas.after(GUI.UPDATE_INTERVAL, self._update)
        self.root.mainloop()
