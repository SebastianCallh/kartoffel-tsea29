from bt_client import BT_client
from gui import GUI
import queue_handlers
import inbound
import outbound
from protocol import *
from eventbus import EventBus
import datetime


DATA_REQUEST_INTERVAL = 1  # seconds

gui = None
last_data_request_time = datetime.datetime.now()


def run_bt_client(queue_handler):
    bt_client = BT_client(queue_handler)
    bt_client.start()


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


def setup_subscriptions():
    EventBus.subscribe(RETURN_PI_IP, printIP)
    EventBus.subscribe(BT_RETURN_SENSOR_DATA, add_sensor_data)
    EventBus.subscribe(BT_RETURN_SERVO_DATA, add_servo_data)
    EventBus.subscribe(BT_RETURN_MAP_DATA, update_map)

def request_data():
    outbound.bt_request_sensor_data()
    outbound.bt_request_servo_data()
    outbound.bt_request_map_data()

def update():
    global gui, last_data_request_time
    EventBus.receive()
    if (datetime.datetime.now() - last_data_request_time) > datetime.timedelta(
            seconds=DATA_REQUEST_INTERVAL):
        print("request sensor data")
        request_data()
        last_data_request_time = datetime.datetime.now()
    gui.canvas.after(GUI.UPDATE_INTERVAL, update)
    
def start_gui():
    global gui
    gui.canvas.after(gui.UPDATE_INTERVAL, update)
    gui.root.mainloop()

def main():
    global gui
    queue_handler = EventBus.queue_handler
    setup_subscriptions()
    run_bt_client(queue_handler)
    gui = GUI()
    start_gui()


main()
