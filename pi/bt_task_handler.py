import pickle

# Files in which to store BT_task objects in transition
# NOTE: If multiple instances of bt_server_intermediary
# are running simultaneously, the may erase each others
# content
to_server_queue = open("to_server.txt", "wb")
from_server_queue = open("from_server.txt", "wb")


class BT_task:

    # NOTE If the client always asks for certain data
    # it might not need to check it when it arrives?

    def __init__(self, cmd_id, data=0):
        self.cmd_id = cmd_id
        self.data = data


def post(cmd_id, data=0):
    task = BT_task(cmd_id, data)
    pickle.dump(task, from_server_queue)


def pop():
    task = pickle.load(to_server_queue)
    return (task.cmd_id, task.data)
