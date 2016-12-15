from gui import GUI
import outbound
from protocol import *
from eventbus import EventBus
import datetime
from ast import literal_eval
import random

try:
    from bt_client import BT_client
    bluetooth_enabled = True
except:
    bluetooth_enabled = False

DATA_REQUEST_INTERVAL = 500  # milliseconds
IP_REQUEST_INTERVAL = 10     # seconds
UPDATE_INTERVAL = 250        # milliseconds

gui = None
bt_client = None
request_type = 0
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


def update_selected_mode(mode):
    gui.update_selected_mode(mode)


def setup_subscriptions():
    EventBus.subscribe(RETURN_PI_IP, update_ip)
    EventBus.subscribe(BT_RETURN_SENSOR_DATA, add_sensor_data)
    EventBus.subscribe(BT_RETURN_SERVO_DATA, add_servo_data)
    EventBus.subscribe(BT_RETURN_MAP_DATA, update_map)
    EventBus.subscribe(CMD_MODE_SET, update_selected_mode)


def request_data():
    global last_ip_request_time, request_type
    if request_type == 0:
        outbound.bt_request_sensor_data()
        request_type = 1
    else:
        outbound.bt_request_servo_data()
        request_type = 0
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
                    milliseconds=DATA_REQUEST_INTERVAL):
                if bt_client is not None and bt_client.is_connected:
                    request_data()

                last_data_request_time = datetime.datetime.now()
        else:
            gui.setup_after_main_loop()
        gui.canvas.after(UPDATE_INTERVAL, update)
    else:
        print("Exit gui in client main")
        outbound.bt_restart()
        while bt_client is not None and not bt_client.restart_demanded:
            pass
        gui.close_window()


def start_gui():
    global gui
    gui.canvas.after(UPDATE_INTERVAL, update)
    gui.root.mainloop()


def main():
    global gui
    queue_handler = EventBus.queue_handler
    setup_subscriptions()

    # MacOS has no support for PyBluez so by disabling the use of it we
    # can still provide a semi-functional experience for Mac users.
    if bluetooth_enabled:
        run_bt_client(queue_handler)
    else:
        print('NOTICE: PyBluez module could not be loaded!')
        print('Bluetooth functionality has been disabled.')

    gui = GUI()
    start_gui()

try:
    main()
except:
    print("Some error in client main")
    outbound.bt_restart()
    while bt_client is not None and not bt_client.restart_demanded:
        pass
    gui.close_window()
