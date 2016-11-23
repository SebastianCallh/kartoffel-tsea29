import pickle
# import psutil
import traceback, sys


# Files in which to store BT_task objects in transition
def peek_line(f):
    pos = f.tell()
    line = f.readline()
    f.seek(pos)
    return line


class BT_task:
    # NOTE If the client always asks for certain data
    # it might not need to check it when it arrives?

    def __init__(self, cmd_id=0, data=0):
        self.cmd_id = int(cmd_id)
        self.data = data


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
        
    # Remove first command in queue and return it
    try:
        task = pickle.load(command_queue)
        print("Poped task från command with id ", task.cmd_id)
        command_queue = open("bt_commands.txt", "wb")
        command_queue.seek(0)
        command_queue.truncate()
        print("Cleaned commands")
    except EOFError:
        pass
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
    # Remove first command in queue and return it
    try:
        task = pickle.load(answer_queue)
        print("Popade från answers with id ", task.cmd_id)
        answer_queue = open("bt_answers.txt", "wb")
        #Clean file
        answer_queue.seek(0)
        answer_queue.truncate()
        print("Clean answers")
    except EOFError:
        #print("EOF pop outgoing")
        pass
    answer_queue.close()
    return task

