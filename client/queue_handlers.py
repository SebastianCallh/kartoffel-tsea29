import queue

QUEUE_MAX_SIZE = 20


class Queue_handler:
    def __init__(self):
        (self.in_queue, self.out_queue) = self.create_task_queues()

    def create_task_queues(self):
        self.in_queue = queue.Queue(QUEUE_MAX_SIZE)
        self.out_queue = queue.Queue(QUEUE_MAX_SIZE)
        return (self.in_queue, self.out_queue)

    def pop_in_queue(self):
        try:
            next_task = self.in_queue.get(False)
            self.in_queue.task_done()
        except queue.Empty:
            next_task = None
        return next_task

    def post_in_queue(self, task):
        try:
            self.in_queue.put(task, timeout=0.75)
        except queue.Full:
            print("in_queue is full")

    def pop_out_queue(self):
        try:
            next_task = self.out_queue.get(False)
            self.out_queue.task_done()
        except queue.Empty:
            next_task = None
        return next_task

    def post_out_queue(self, task):
        try:
            self.out_queue.put(task, timeout=0.75)
        except queue.Full:
            print("out_queue is full")
