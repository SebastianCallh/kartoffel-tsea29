import pickle

def clean_queue_files():
    # Create files or erase previous content
    answer_queue = open("bt_answers.txt", "w")
    answer_queue.seek(0)
    answer_queue.truncate()
    command_queue = open("bt_commands.txt", "w")
    command_queue.seek(0)
    command_queue.truncate()
    answer_queue.close()
    command_queue.close()


# kallas från main
def post_outgoing(bt_task):
    global busy_outgoing
    print("in post_outgoing and dumpint task with id", bt_task.cmd_id)
    answer_queue = open("bt_answers.txt", "wb")
    print("could open file")
    pickle.dump(bt_task, answer_queue)
    print("have dumped to pickle!")
    answer_queue.close()
    print("closing file and returning to main!")


# kallas från main
def pop_incoming():
    command_queue = open("bt_commands.txt", "rb")
    task = None

    task_q = []
    while (True):
        try:
            task_i = pickle.load(command_queue)
            task_q.append(task_i)
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


# kallas från server
def post_incoming(bt_task):
    command_queue = open("bt_commands.txt", "wb")
    print("task type in post_incoming ", type(bt_task))
    pickle.dump(bt_task, command_queue)
    print("Could dump to pickle in post_incoming")
    # pickle.Pickler.clear_memo(self=)
    command_queue.close()
    print("Closing file and return to bt_server")


# kallas från server
def pop_outgoing():
    answer_queue = open("bt_answers.txt", "rb")
    task = None

    task_q = []
    while (True):
        try:
            task_i = pickle.load(answer_queue)
            task_q.append(task_i)
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
