from queue import Queue

import protocol
import outbound
from eventbus import EventBus
from bt_client import BT_client
from gui import GUI


QUEUE_MAX_SIZE = 20


def create_task_queues():
    in_queue = Queue(QUEUE_MAX_SIZE)
    out_queue = Queue(QUEUE_MAX_SIZE)
    return (in_queue,out_queue)
    
def setup_subscriptions():
    EventBus.subscribe(RETURN_PI_IP, gui.printIP)
    EventBus.subscribe(BT_RETURN_SENSOR_DATA, gui.add_sensor_data)
    EventBus.subscribe(BT_RETURN_SERVO_DATA, gui.add_servo_data)
    EventBus.subscribe(BT_RETURN_MAP_DATA, gui.update_map)

def run_bt_client(in_queue, out_queue):
    bt_client = BT_client(in_queue, out_queue)
    bt_client.start()

def main():
    (in_queue,out_queue) = create_task_queues()
    run_bt_client(in_queue,out_queue)
    gui = GUI()    
    setup_subscriptions()
    gui.start()
    
    
main()
