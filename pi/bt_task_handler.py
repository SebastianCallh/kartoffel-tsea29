import pickle
import shutil

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

# kallas från main
def post_outgoing(bt_task):  
    answer_queue = open("bt_answers.txt", "ab")
    pickle.dump(bt_task, answer_queue)

# kallas från main
def pop_incoming():
    command_queue = open("bt_commands.txt", "rb")
    try: 
        task = pickle.load(command_queue)
        
        # Remove first command in queue
        tasks = command_queue.readlines()
        del tasks[0]
        target_command_queue = open("bt_commands.txt","wb")
        target_command_queue.writelines(tasks)
        #print("task typ ar: ", type(task))
    except EOFError:
        task = None
    #print("task värde på id: ", task.cmd_id)
    return task
    
# kallas från server
def post_incoming(bt_task):
    command_queue = open("bt_commands.txt", "ab")
    print("task type in post_incoming ", type(bt_task))
    pickle.dump(bt_task, command_queue)

# kallas från server
def pop_outgoing():
    answer_queue = open("bt_answers.txt", "rb")
    try:
        task = pickle.load(answer_queue)
        
        # Remove first command in queue
        tasks = answer_queue.readlines()
        del tasks[0]
        target_answer_queue = open("bt_answers.txt","wb")
        target_answer_queue.writelines(tasks)
    except EOFError:
        task = None
    return task
    

