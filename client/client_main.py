import queue
from protocol import *
import inbound
from eventbus import EventBus
from bt_client import BT_client
from gui import GUI

QUEUE_MAX_SIZE = 20


def create_task_queues():
    in_queue = queue.Queue(QUEUE_MAX_SIZE)
    out_queue = queue.Queue(QUEUE_MAX_SIZE)
    return (in_queue, out_queue)


(in_queue, out_queue) = create_task_queues()


def setup_subscriptions():
    EventBus.subscribe(RETURN_PI_IP, inbound.printIP)
    EventBus.subscribe(BT_RETURN_SENSOR_DATA, inbound.add_sensor_data)
    EventBus.subscribe(BT_RETURN_SERVO_DATA, inbound.add_servo_data)
    EventBus.subscribe(BT_RETURN_MAP_DATA, inbound.update_map)


def run_bt_client(in_queue, out_queue):
    bt_client = BT_client(in_queue, out_queue)
    bt_client.start()


def main():
    (in_queue, out_queue) = create_task_queues()
    run_bt_client(in_queue, out_queue)
    gui = GUI()
    inbound.gui = gui
    setup_subscriptions()
    gui.start()


main()
