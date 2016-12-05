from bt_client import BT_client
from gui import GUI
import outbound
from protocol import *
from eventbus import EventBus
import datetime
import random

DATA_REQUEST_INTERVAL = 1  # seconds
UPDATE_INTERVAL = 250  # milliseconds

gui = None
last_data_request_time = datetime.datetime.now()


def run_bt_client(queue_handler):
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
    gui.update_map(data)


def setup_subscriptions():
    EventBus.subscribe(RETURN_PI_IP, update_ip)
    EventBus.subscribe(BT_RETURN_SENSOR_DATA, add_sensor_data)
    EventBus.subscribe(BT_RETURN_SERVO_DATA, add_servo_data)
    EventBus.subscribe(BT_RETURN_MAP_DATA, update_map)


def request_data():
    outbound.bt_request_sensor_data()
    outbound.bt_request_servo_data()
    # outbound.bt_request_map_data()
    outbound.request_ip()


def update():
    global gui, last_data_request_time
    if not gui.exit_demanded:
        #EventBus.receive()
        if (datetime.datetime.now() - last_data_request_time) > datetime.timedelta(
                seconds=DATA_REQUEST_INTERVAL):
            #request_data()
            x1 = int(input("x: "))
            if x1 == 0:
                print("Close gui")
                gui.close_window()
                return
            y1 = int(input("y: "))
            '''x2 = int(input("x2: "))
            y2 = int(input("y2: "))

            gui.update_map([(x1, y1), (x2, y2)])'''
            gui.update_map([(x1, y1)])
            #gui.canvas.create_line(x1,y1,x2,y2,fill="black")
            print("canvas size ", gui.canvas.winfo_height(), " ", gui.canvas.winfo_width())
            last_data_request_time = datetime.datetime.now()
        gui.canvas.after(UPDATE_INTERVAL, update)
    else:
        print("Exit gui in client main")
        outbound.bt_shutdown()
        gui.close_window()


def start_gui():
    global gui
    gui.canvas.after(UPDATE_INTERVAL, update)
    gui.root.mainloop()


def main():
    global gui
    queue_handler = EventBus.queue_handler
    setup_subscriptions()
    #run_bt_client(queue_handler)
    gui = GUI()
    start_gui()


main()
