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
    # answer_queue.seek(0)
    # answer_queue.truncate()
    command_queue = open("bt_commands.txt", "w")
    # command_queue.seek(0)
    # command_queue.truncate()
    answer_queue.close()
    command_queue.close()


# kallas från main
def post_outgoing(bt_task):
    print("in post_outgoing")
    answer_queue = open("bt_answers.txt", "ab")
    print("could open file")
    pickle.dump(bt_task, answer_queue)
    print("have dumped to pickle!")
    answer_queue.close()
    print("closing file and returning to main!")


# kallas från main
def pop_incoming():
    command_queue = open("bt_commands.txt", "rb")
    next_task = None
    '''try:
        # psutil.phymem_usage()
        #print("peek incoming command_queue: ", peek_line(command_queue))
        task = pickle.load(command_queue)       
        # print("task typ ar: ", type(task))
    except EOFError:
        pass
    except MemoryError:
        print("pop_in: error = ", str(MemoryError))
        # psutil.phymem_usage()
        traceback.print_exc(file=sys.stdout)
        task = None'''
        
    # Remove first command in queue and return it
    tasks = []
    while(True):
        try:
            task = pickle.load(command_queue)
            tasks.append(task)
        except EOFError:
            break
    command_queue = open("bt_commands.txt", "wb")
    if tasks:
        next_task = tasks[0]
        print("Poppar task med id från cmds ",next_task.cmd_id)
        del tasks[0]
        for task in tasks:
            print("Lagger tillbaks task med id ", task.cmd_id, " i cmd queue")
            pickle.dump(task,command_queue)
    command_queue.close()
    return next_task


# kallas från server
def post_incoming(bt_task):
    command_queue = open("bt_commands.txt", "ab")
    print("task type in post_incoming ", type(bt_task))
    pickle.dump(bt_task, command_queue)
    print("Could dump to pickle in post_incoming")
    # pickle.Pickler.clear_memo(self=)
    command_queue.close()
    print("Closing file and return to bt_server")


# kallas från server
def pop_outgoing():
    answer_queue = open("bt_answers.txt", "rb")
    next_task = None
    '''try:
        # psutil.phymem_usage()
        #print("peek outgoing command_queue: ", peek_line(answer_queue))
        task = pickle.load(answer_queue)
        #print("Able to load, task-ID =", task.cmd_id)
        # psutil.phymem_usage()
        # Remove first command in queue
        tasks = answer_queue.readlines()
        print("tasks out=", tasks)
        if tasks:
            del tasks[0]
            target_answer_queue = open("bt_answers.txt","wb")
            target_answer_queue.writelines(tasks)
            target_answer_queue.close()
    except EOFError:
        pass
    except MemoryError:
        print("pop_in: error = ", str(MemoryError))
        # psutil.phymem_usage()
        traceback.print_exc(file=sys.stdout)
        task = None'''
    # Remove first command in queue and return it
    tasks = []
    while(True):
        try:
            task = pickle.load(answer_queue)
            tasks.append(task)
        except EOFError:
            break
    answer_queue = open("bt_answers.txt", "wb")
    if tasks:
        next_task = BT_task(tasks[0].cmd_id, tasks[0].data)
        print("Poppar task med id från ans",next_task.cmd_id)
        del tasks[0]
        for task in tasks:
            pickle.dump(task,answer_queue)
            print("Lagger tillbaks task från med id ", task.cmd_id, " i ans queue")
    answer_queue.close()
    return next_task

