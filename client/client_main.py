from bt_client import BT_client
from gui import GUI
import queue_handlers
import inbound
from protocol import *

gui = None


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


def setup_subscriptions(eventbus):
    eventbus.subscribe(RETURN_PI_IP, printIP)
    eventbus.subscribe(BT_RETURN_SENSOR_DATA, add_sensor_data)
    eventbus.subscribe(BT_RETURN_SERVO_DATA, add_servo_data)
    eventbus.subscribe(BT_RETURN_MAP_DATA, update_map)


def main():
    queue_handler = queue_handlers.Queue_handler()
    setup_subscriptions(queue_handler.eventbus)
    run_bt_client(queue_handler)
    gui = GUI(queue_handler)
    inbound.gui = gui
    gui.start()


main()
