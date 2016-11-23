import bt_server
import bt_server_cmds
import bt_task_handler
import protocol
from datetime import datetime

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1

log = open("log.txt", "w")


def setup_server():
    global log
    # log.write("In main" + str(datetime.now()))
    server = bt_server.BT_Server(PI_ADDR, PORT, BACKLOG)
    print("before accept_connection")
    server.accept_connection()
    print("after accept_connection")
    bt_task_handler.clean_queue_files()
    return server


"""
  The main function initialize the server and runs it. 
  The function handles the flow of information between
  the intermediary, server and client. 
"""

def run(server):
    exit = False
    while not exit:
        # Loop and wait for server commands
        has_new_incoming = server.update_incoming()
        # TODO Change assumption that data only contains ID!!
        if has_new_incoming:
            print("bt_runner: has new incoming!")
            print("Data = " + server.incoming_data)
            if has_new_incoming == bt_server.BT_EOF:
                server.shutdown_server()

            if int(server.incoming_data) == protocol.BT_SERVER_RESTART:
                print("Starting to restart")
                # server.shutdown_server()
                del server
                server = setup_server()
                continue
            elif int(server.incoming_data) == protocol.BT_SERVER_SHUTDOWN:
                print("Setting exit to true")
                exit = True
                continue
            server.post_to_incoming()
            print("posted to incoming")

        has_new_outgoing = server.update_outgoing()
        if (has_new_outgoing):
            print("bt_runner: sending data")
            server.send_data()
    return xx # TODO Should return values based on restart or shutdown



def main():
    global log

    server = setup_server()
    xx = run(server)



    print("out while not exit loop")
    #server.shutdown_server()
    #del server




main()
