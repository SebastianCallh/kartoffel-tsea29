from bt_client import BT_client
from gui import GUI
import outbound
from protocol import *
from eventbus import EventBus
import datetime
from ast import literal_eval
import random

DATA_REQUEST_INTERVAL = 1  # seconds
IP_REQUEST_INTERVAL = 10   # seconds
UPDATE_INTERVAL = 250      # milliseconds
TEST_CORNERS = [(0, 0), (0,1), (1, 1), (1, 3), (-3, 3), (-3, 4),
                (-2, 4), (-2, 5), (-4, 5), (-4, 7), (5, 7), (5, 9),
                (7, 9), (7, 5), (4, 5), (4, -4), (-15, -4), (-15, -3), (3, -3),
                (3, 0), (0, 0), (1, 4), (3, 4), (3, 6), (1, 6), (1, 4)]

TEST_CORNERS2 = [(0,0), (1,0), (1,-1),(1,-2),(1,3),(0,3),(-1,3),(-2,3),(-2,2),(-1,2),(0,2),(0,1),(0,0)]

curr_test_corn = 0

gui = None
bt_client = None
last_data_request_time = datetime.datetime.now()
last_ip_request_time = datetime.datetime.now()


def run_bt_client(queue_handler):
    global bt_client
    bt_client = BT_client(queue_handler)
    bt_client.start()


def update_ip(data):
    global gui
    gui.update_ip(data)


def add_sensor_data(data):
    global gui
    gui.add_sensor_data(data)


def add_servo_data(data):
    global gui
    gui.add_servo_data(data)


def update_map(data):
    global gui
    print(data)
    gui.update_map(data)


def setup_subscriptions():
    EventBus.subscribe(RETURN_PI_IP, update_ip)
    EventBus.subscribe(BT_RETURN_SENSOR_DATA, add_sensor_data)
    EventBus.subscribe(BT_RETURN_SERVO_DATA, add_servo_data)
    EventBus.subscribe(BT_RETURN_MAP_DATA, update_map)


def request_data():
    global last_ip_request_time
    outbound.bt_request_sensor_data()
    outbound.bt_request_servo_data()
    outbound.bt_request_map_data()
    if (datetime.datetime.now() - last_ip_request_time) > datetime.timedelta(
            seconds=IP_REQUEST_INTERVAL):
        outbound.request_ip()
        last_ip_request_time = datetime.datetime.now()
    pass


def update():
    global gui, last_data_request_time, curr_test_corn, bt_client
    if not gui.exit_demanded:
        if gui.finished_setup:
            EventBus.receive()
            if (datetime.datetime.now() - last_data_request_time) > datetime.timedelta(
                    seconds=DATA_REQUEST_INTERVAL):
                if bt_client.is_connected:
                    request_data()

                """gui.update_map([TEST_CORNERS2[curr_test_corn]])
                if curr_test_corn < len(TEST_CORNERS2) -1:
                    curr_test_corn += 1"""
                last_data_request_time = datetime.datetime.now()
        else:
            gui.setup_after_main_loop()
        gui.canvas.after(UPDATE_INTERVAL, update)
    else:
        print("Exit gui in client main")
        outbound.bt_restart()
        while not bt_client.restart_demanded:
            pass
        gui.close_window()


def start_gui():
    global gui
    gui.canvas.after(UPDATE_INTERVAL, update)
    gui.root.mainloop()


def main():
    global gui
    print("1")
    queue_handler = EventBus.queue_handler
    print("2")
    setup_subscriptions()
    print("3")
    run_bt_client(queue_handler)
    print("4")
    gui = GUI()
    print("5")
    start_gui()
    print("6")

try:
    main()
except:
    print("Some error in client main")
    '''outbound.bt_restart()
    while not bt_client.restart_demanded:
        pass'''
    gui.close_window()
