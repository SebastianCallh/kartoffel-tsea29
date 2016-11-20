import pickle

# Files in which to store BT_task objects in transition
# NOTE: If multiple instances of bt_server_intermediary
# are running simultaneously, the may erase each others
# content
to_server_queue = None
from_server_queue = None


class BT_task:

    # NOTE If the client always asks for certain data
    # it might not need to check it when it arrives?

    def __init__(self, cmd_id = 0, data = 0):
        self.cmd_id = cmd_id
        self.data = data
        
def open_medetiary_files():
    global to_server_queue
    global from_server_queue
    to_server_queue = open("to_server.txt", "wb+")
    from_server_queue = open("from_server.txt", "wb+")
    

# kallas från main
def post_outgoing(bt_task):  
    global from_server_queue
    pickle.dump(bt_task, from_server_queue)

# kallas från main
def pop_incoming():
    global to_server_queue
    try:
        task = pickle.load(to_server_queue)
    except EOFError:
        task = None
    return task
    
# kallas från server
def post_incoming(bt_task):
    global to_server_queue
    pickle.dump(bt_task, to_server_queue)

# kallas från server
def pop_outgoing():
    global from_server_queue
    try:
        task = pickle.load(from_server_queue)
    except EOFError:
        task = None
    return task
    

