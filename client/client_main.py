import tkinter
from queue import Queue

import protocol
import outbound
from eventbus import EventBus
from bt_client import BT_client
import gui


QUEUE_MAX_SIZE = 20

CANVAS_X_SIZE = 500
CANVAS_Y_SIZE = 500



def create_task_queues():
    in_queue = Queue(QUEUE_MAX_SIZE)
    out_queue = Queue(QUEUE_MAX_SIZE)
    return (in_queue,out_queue)
    
def setup_subscriptions():
    EventBus.subscribe(RETURN_PI_IP, printIP)
    EventBus.subscribe(BT_RETURN_SENSOR_DATA, add_sensor_data)
    EventBus.subscribe(BT_RETURN_SERVO_DATA, add_servo_data)
    EventBus.subscribe(BT_RETURN_MAP_DATA, update_map)

def run_bt_client(in_queue, out_queue):
    bt_client = BT_client(in_queue, out_queue)
    bt_client.run()

def start_GUI():
    root = Tk()
    canvas = Canvas(root,CANVAS_X_SIZE,CANVAS_Y_SIZE)
    canvas.pack()

def main():
    (in_queue,out_queue) = create_task_queues()
    setup_subscriptions()
    
    run_bt_client(in_queue,out_queue)
    start_GUI()
    
    
main()
