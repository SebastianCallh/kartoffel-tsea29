import pickle
from bt_task import BT_task


def clean_queue_files():
    """
    Creates clean files for queues between server and main unit.
    """
    answer_queue = open("bt_answers.txt", "w")
    answer_queue.seek(0)
    answer_queue.truncate()
    command_queue = open("bt_commands.txt", "w")
    command_queue.seek(0)
    command_queue.truncate()
    answer_queue.close()
    command_queue.close()


def post_outgoing(task):
    """
    Called from main unit.
    Posts BT_task processed by main unit to answer queue.
    """
    answer_queue = open("bt_answers.txt", "wb")
    pickle.dump(task, answer_queue)
    print("post_outgoing, could post to pickle!")
    answer_queue.close()


def pop_incoming():
    """
    Called from main unit.
    Pops and returns next BT_task from commands queue,
    to be processed by the main unit.
    """
    command_queue = open("bt_commands.txt", "rb")
    task = None

    task_q = []
    while (True):
        try:
            task_i = pickle.load(command_queue)
            task_q.append(task_i)
            print("pop_incoming, could load from pickle!")
        except EOFError:
            break
    if task_q:
        task = BT_task(task_q[0].cmd_id, task_q[0].data)
        del task_q[0]
        command_queue = open("bt_commands.txt", "wb")
        for task_i in task_q:
            pickle.dump(task_i, command_queue)

    command_queue.close()
    return task


def post_incoming(task):
    """
    Called from server.
    Posts given BT_task to command queue,
    to be processed by main unit.
    """
    command_queue = open("bt_commands.txt", "wb")
    pickle.dump(task, command_queue)
    print("post_incoming, could dump to pickle!")
    command_queue.close()


def pop_outgoing():
    """
    Called from server.
    Pops next outgoing BT_task from answer queue,
    tasks already processed by main unit.
    Returns popped task.
    """
    answer_queue = open("bt_answers.txt", "rb")
    task = None

    task_q = []
    while (True):
        try:
            task_i = pickle.load(answer_queue)
            task_q.append(task_i)
            print("pop_outgoing, could load from pickle!")
        except EOFError:
            break
    if task_q:
        task = BT_task(task_q[0].cmd_id, task_q[0].data)
        del task_q[0]
        answer_queue = open("bt_answers.txt", "wb")
        for task_i in task_q:
            pickle.dump(task_i, answer_queue)

    answer_queue.close()
    return task
