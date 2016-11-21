import pickle
#import psutil
import traceback, sys

# Files in which to store BT_task objects in transition


class BT_task:

    # NOTE If the client always asks for certain data
    # it might not need to check it when it arrives?

    def __init__(self, cmd_id = 0, data = 0):
        self.cmd_id = int(cmd_id)
        self.data = data
  
def clean_queue_files():
    #Create files or erase previous content
    answer_queue = open("bt_answers.txt","w")
    answer_queue.seek(0)
    answer_queue.truncate()
    command_queue = open("bt_commands.txt","w")
    command_queue.seek(0)
    command_queue.truncate()
    answer_queue.close()
    command_queue.close()

# kallas från main
def post_outgoing(bt_task):  
    answer_queue = open("bt_answers.txt", "ab")
    pickle.dump(bt_task, answer_queue)
    pickle.Pickler.clear_memo()
    answer_queue.close()

# kallas från main
def pop_incoming():
    command_queue = open("bt_commands.txt", "rb")
    try:
        #psutil.phymem_usage()
        task = pickle.load(command_queue)
        print("Able to load, task-ID =", task.cmd_id)
        # Remove first command in queue
        tasks = command_queue.readlines()
        del tasks[0]
        target_command_queue = open("bt_commands.txt","wb")
        target_command_queue.writelines(tasks)
        target_command_queue.close()
        #print("task typ ar: ", type(task))
    except EOFError or MemoryError:
        print("pop_in: error = ", str(MemoryError))
        #psutil.phymem_usage()
        traceback.print_exc(file=sys.stdout)
        task = None
    #print("task värde på id: ", task.cmd_id)
    command_queue.close()
    return task
    
# kallas från server
def post_incoming(bt_task):
    command_queue = open("bt_commands.txt", "ab")
    print("task type in post_incoming ", type(bt_task))
    pickle.dump(bt_task, command_queue)
    pickle.Pickler.clear_memo()
    command_queue.close()

# kallas från server
def pop_outgoing():
    answer_queue = open("bt_answers.txt", "rb")
    try:
        #psutil.phymem_usage()
        task = pickle.load(answer_queue)
        print("Able to load, task-ID =", task.cmd_id)
        #psutil.phymem_usage()
        # Remove first command in queue
        tasks = answer_queue.readlines()
        del tasks[0]
        target_answer_queue = open("bt_answers.txt","wb")
        target_answer_queue.writelines(tasks)
        target_answer_queue.close()
    except EOFError or MemoryError:
        print("pop_out: error = ", str(MemoryError))
        #psutil.phymem_usage()
        task = None
    answer_queue.close()
    return task
    

