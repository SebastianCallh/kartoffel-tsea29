import pickle

# Files in which to store BT_task objects in transition
# NOTE: If multiple instances of bt_server_intermediary
# are running simultaneously, the may erase each others
# content


class BT_task:

    # NOTE If the client always asks for certain data
    # it might not need to check it when it arrives?

    def __init__(self, cmd_id = 0, data = 0):
        self.cmd_id = cmd_id
        self.data = data
  
def clean_queue_files():
    #Create files or erase previous content
    from_server = open("from_server.txt","w")
    to_server = open("to_server.txt","w")

# kallas från main
def post_outgoing(bt_task):  
    from_server_queue = open("from_server.txt", "ab")
    pickle.dump(bt_task, from_server_queue)

# kallas från main
def pop_incoming():
    to_server_queue = open("to_server.txt", "rb")
    try:
        task = pickle.load(to_server_queue)
        print("task typ ar: ", type(task))
    except EOFError:
        task = None
    print("task värde på id: ", task.cmd_id)
    return task
    
# kallas från server
def post_incoming(bt_task):
    to_server_queue = open("to_server.txt", "ab")
    print("task type in post_incoming ", type(bt_task))
    pickle.dump(bt_task, to_server_queue)

# kallas från server
def pop_outgoing():
    from_server_queue = open("from_server.txt", "rb")
    try:
        task = pickle.load(from_server_queue)
    except EOFError:
        task = None
    return task
    

