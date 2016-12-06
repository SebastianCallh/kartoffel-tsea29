from tkinter import *
import outbound
from map_grid import MapGrid
import datetime


class GUI:
    WINDOW_X = 800
    WINDOW_Y = 600
    CANVAS_X = int(WINDOW_X * 0.6)
    CANVAS_Y = CANVAS_X
    LIST_FRAME_X = int(WINDOW_X * 0.3)
    LIST_FRAME_Y = int(WINDOW_Y * 0.75)
    LIST_BOX_Y = int(LIST_FRAME_Y * 0.5)
    LIST_BOX_X = int(LIST_FRAME_X * 0.5)
    BTN_FRAME_X = int(WINDOW_X)
    BTN_FRAME_Y = int(WINDOW_Y * 0.2)
    BG_COLOR = "orange"

    MAX_LIST_ITEMS = 13
    MIN_TIME_KEY_EVENT = 500            # milliseconds

    def __init__(self):
        self.pi_ip = ""
        self.exit_demanded = False

        self.map_grid = MapGrid()

        self.root = Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.title("Kartoffel control")
        self.main_frame = Frame(self.root, width=self.WINDOW_X, height=self.WINDOW_Y, bg=self.BG_COLOR)
        self.main_frame.focus_set()  # Set all frame as listening to keyboard events
        self.main_frame.grid()

        # Keybindings
        # Run functions when certain keys are pressed. Bind to same as buttons.
        #TODO Varför olika?
        self.main_frame.bind('<w>', self.forward)
        self.root.bind('<Up>', self.forward)
        self.main_frame.bind('<s>', self.back)
        self.root.bind('<Down>', self.back)
        self.main_frame.bind('<a>', self.left)
        self.root.bind('<Left>', self.left)
        self.main_frame.bind('<d>', self.right)
        self.root.bind('<Right>', self.right)
        self.main_frame.bind('<q>', self.forward_left)
        self.main_frame.bind('<e>', self.forward_right)

        self.last_key_event_time = datetime.datetime.now()

        # --- Canvas ---
        self.canvas = Canvas(self.main_frame,
                             width=GUI.CANVAS_X,
                             height=GUI.CANVAS_Y, bg="white")
        self.canvas.grid(column=0, row=0, padx=10,pady=10)

        # --- Lists ---
        self.list_frame = Frame(self.main_frame, width=self.LIST_FRAME_X, height=self.LIST_FRAME_Y,
                                bg=self.BG_COLOR)
        self.list_frame.grid(row=0, column=1, padx=10)

        self.ir_list = Listbox(self.list_frame, height=self.MAX_LIST_ITEMS)
        self.ir_list.grid(row=1, column=0)
        self.ir_list_nr_items = 0
        self.ir_label = Label(self.list_frame, text="IR data (mm) \n (left_back, left, right, right_back)",
                              fg="black", bg=self.BG_COLOR)
        self.ir_label.grid(row=0, column=0)

        self.laser_list = Listbox(self.list_frame, height=self.MAX_LIST_ITEMS)
        self.laser_list.grid(row=1, column=1)
        self.laser_list_nr_items = 0
        self.laser_label = Label(self.list_frame, text="Laser data", fg="black", bg=self.BG_COLOR)
        self.laser_label.grid(row=0, column=1)

        self.gyro_list = Listbox(self.list_frame, height=self.MAX_LIST_ITEMS)
        self.gyro_list.grid(row=3, column=0)
        self.gyro_list_nr_items = 0
        self.gyro_label = Label(self.list_frame, text="Gyro data \n (degrees)", fg="black", bg=self.BG_COLOR)
        self.gyro_label.grid(row=2, column=0)

        self.servo_list = Listbox(self.list_frame, height=self.MAX_LIST_ITEMS)
        self.servo_list.grid(row=3, column=1)
        self.servo_list_nr_items = 0
        self.servo_label = Label(self.list_frame, text="Servo data \n (speed)", fg="black", bg=self.BG_COLOR)
        self.servo_label.grid(row=2, column=1)

        # --- Buttons ---
        self.btn_frame = Frame(self.main_frame, width=self.BTN_FRAME_X, height=self.BTN_FRAME_Y)
        self.btn_frame.grid(row=1, column=0, pady=10, padx=10)

        self.btn_forward = Button(self.btn_frame, text="Forward", command=self.forward)
        self.btn_forward.grid(row=1, column=2)

        self.btn_back = Button(self.btn_frame, text="Back", command=self.back)
        self.btn_back.grid(row=1, column=3)

        self.btn_right = Button(self.btn_frame, text="Right", command=self.right)
        self.btn_right.grid(row=1, column=4)

        self.btn_left = Button(self.btn_frame, text="Left", command=self.left)
        self.btn_left.grid(row=1, column=1)

        self.btn_forward_right = Button(self.btn_frame, text="Forward left", command=self.forward_left)
        self.btn_forward_right.grid(row=0, column=2, padx=5, pady=5)

        self.btn_forward_left = Button(self.btn_frame, text="Forward right", command=self.forward_right)
        self.btn_forward_left.grid(row=0, column=3, padx=5, pady=5)

        self.bt_restart = Button(self.btn_frame, text="Restart bluetooth\nconnection",
                                                command=outbound.bt_restart)
        self.bt_restart.grid(row=1,column=5,padx=10, pady=10)

        self.ip_box = Label(self.main_frame, text="Pi IP: ", width=25, bg="white")
        self.ip_box.grid(row=1, column=1)

        # --- Image ----
        logo = PhotoImage(file="Logo.gif")
        self.resampled_logo = logo.subsample(3, 4)
        self.logo_box = Label(self.btn_frame, image=self.resampled_logo)
        self.logo_box.grid(row=1, column=0, padx=10)

    '''
    Values should be a list containing of [ir_left,ir_right,ir_left_back,
    ir_right_back,laser,gyro]
    '''
    def add_sensor_data(self, values):
        ir_values = str(values[2]) + ", " + str(values[0]) + ", " + str(values[1]) + ", " + str(values[3])

        self.ir_list.insert(0, ir_values)
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
            for i in range(1, self.MAX_LIST_ITEMS):
                item = self.servo_list.get(i)
                self.servo_list.insert(i - 1, item)
        else:
            self.servo_list_nr_items += 1
        self.servo_list.insert(END, str(values[0]) + ', ' + str(values[1]))
        print("Servo data: ", str(values))

    def update_map(self, values):
        print("Map data: ", str(values))
        self.map_grid.update_map(values, self.canvas)

    '''
    Ip expected to be in format [ip]
    '''
    def update_ip(self, ip):
        print("IP i gui: ", str(ip[0]))
        self.ip_box.config(text="Pi IP: " + str(ip[0]))
        
    def exit(self):
        self.exit_demanded = True
        print("Exit gui")
        
    def close_window(self):
        self.root.destroy()

    def check_key_event_time(self):
        return (datetime.datetime.now() - self.last_key_event_time) > datetime.timedelta(
                        milliseconds=self.MIN_TIME_KEY_EVENT)

    '''Functions for handling key press.
    Takes forced event, but ignores it and calls correct driver function.
    '''
    def forward(self, event=None):
        self.event_handler(outbound.bt_drive_forward, event=event, repetition=5)

    def back(self, event=None):
        self.event_handler(outbound.bt_drive_back, event=event, repetition=5)

    def left(self, event=None):
        self.event_handler(outbound.bt_turn_left, event=event, repetition=5)

    def right(self, event=None):
        self.event_handler(outbound.bt_turn_right, event=event, repetition=5)

    def forward_right(self, event=None):
        self.event_handler(outbound.bt_forward_right, event=event, repetition=5)

    def forward_left(self, event=None):
        self.event_handler(outbound.bt_forward_left, event=event, repetition=5)

    '''
    Makes sure event can not occur faster than a predefined time interval.
    If event argument is left out, event_handler will interpret that as if
    it was called from a button and call the command function several times.
    '''
    def event_handler(self, command, **options):
        if self.check_key_event_time():
            if not options["event"]:
                for i in range(0, options["repetition"]):
                    while not self.check_key_event_time():
                        continue
                    command()
                    self.last_key_event_time = datetime.datetime.now()
            else:
                command()
                self.last_key_event_time = datetime.datetime.now()
