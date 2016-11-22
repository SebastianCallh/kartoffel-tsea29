import bt_server
import bt_server_cmds
import bt_task_handler
import protocol
from datetime import datetime

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1

log = open("log.txt","w")


def setup_server():
    global log
    #log.write("In main" + str(datetime.now()))
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
def main():
    global log
    server = setup_server()

    # TODO add exit/restart options (conditions in loop)
    while True:
        # Loop and wait for server commands
        has_new_incoming = server.update_incoming()
        # TODO Change assumption that data only contains ID!!
        if has_new_incoming:
            print("bt_runner: has new incoming!")
            print("Data = " + server.incoming_data)
            if server.incoming_data == protocol.BT_SERVER_RESTART:
                server.shutdown_server()
                del server
                server = setup_server()
                continue
            elif server.incoming_data == protocol.BT_SERVER_EXIT:
                break
            server.post_to_incoming()
            print("posted to incoming")

        has_new_outgoing = server.update_outgoing()
        if (has_new_outgoing):
            print("bt_runner: sending data")
            server.send_data()

    #server.shutdown_server()
    #del server
    """busy = False

    # TODO add exit/restart options (conditions in loop)
    while True:
        # Loop and wait for server commands
        while not busy:
            has_new_incoming = server.update_incoming()
            # TODO Change assumption that data only contains ID!!
            if has_new_incoming:
                print("bt_runner: has new incoming!")
                print("Data = " + server.incoming_data)
                cmd_type = bt_server_cmds.validate_cmd(server.incoming_data)
                print("Cmd id in runner-main: " + cmd_type)
                if cmd_type == "":
                    print("Runner: cmd_type == empty")
                    continue
                elif cmd_type == "rqst":
                    print("Runner: cmd_type == rqst")
                    busy = True
                elif cmd_type == "direct":
                    print("Runner: cmd_typ == direct")
                else:
                    print("Runner: cmd_type is something unknown")
                    continue
                server.post_to_incoming()
                print("posted to incoming")

        has_new_outgoing = server.update_outgoing()
        if (has_new_outgoing):
            print("bt_runner: sending data")
            server.send_data()
            busy = False"""


main()
