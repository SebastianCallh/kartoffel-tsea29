import bt_server
import bt_server_cmds
import bt_task_handler
from datetime import datetime

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1

"""
  The main function initialize the server and runs it. 
  The function handles the flow of information between
  the intermediary, server and client. 
"""


def main():
    log = open("log.txt","w")
    log.write("In main" + str(datetime.now()))

    server = bt_server.BT_Server(PI_ADDR, PORT, BACKLOG)
    log.write("before accept_connection")
    server.accept_connection()
    log.write("after accept_connection")
    bt_task_handler.clean_queue_files()


    '''# TODO add exit/restart options (conditions in loop)
    while True:
        # Loop and wait for server commands
        has_new_incoming = server.update_incoming()
        # TODO Change assumption that data only contains ID!!
        if has_new_incoming:
            log.write("bt_runner: has new incoming!")
            log.write("Data = " + server.incoming_data)
            server.post_to_incoming()
            log.write("posted to incoming")

        has_new_outgoing = server.update_outgoing()
        if (has_new_outgoing):
            log.write("bt_runner: sending data")
            server.send_data()'''

    busy = False

    # TODO add exit/restart options (conditions in loop)
    while True:
        # Loop and wait for server commands
        while not busy:
            has_new_incoming = server.update_incoming()
            # TODO Change assumption that data only contains ID!!
            if has_new_incoming:
                log.write("bt_runner: has new incoming!")
                log.write("Data = " + server.incoming_data)
                cmd_type = bt_server_cmds.validate_cmd(server.incoming_data)
                log.write("Cmd id in runner-main: " + cmd_type)
                if cmd_type == "":
                    continue
                elif cmd_type == "rqst":
                    busy = True
                server.post_to_incoming()
                log.write("posted to incoming")

        has_new_outgoing = server.update_outgoing()
        if (has_new_outgoing):
            log.write("bt_runner: sending data")
            server.send_data()
            busy = False


main()
