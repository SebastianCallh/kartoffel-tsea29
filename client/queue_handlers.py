import queue



def pop_in_queue():
    try:
        next_task = in_queue.get(False)
    except queue.Empty:
        next_task = None
    return next_task


def post_in_queue(task):
    try:
        in_queue.put(task, timeout=0.75)
    except queue.Full:
        print("in_queue is full")


def pop_out_queue():
    try:
        next_task = out_queue.get(False)
    except queue.Empty:
        next_task = None
    return next_task


def post_out_queue(task):
    try:
        out_queue.put(task, timeout=0.75)
    except queue.Full:
        print("out_queue is full")