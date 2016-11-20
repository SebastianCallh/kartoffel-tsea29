import bt_server
import bt_server_cmds
import bt_task_handler

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1

"""
  The main function initialize the server and runs it. 
  The function handles the flow of information between
  the intermediary, server and client. 
"""


def main():
    busy = False

    server = bt_server.BT_Server(PI_ADDR, PORT, BACKLOG)
    print("before accept_connection")
    server.accept_connection()
    print("after accept_connection")

    # TODO add exit/restart options (conditions in loop)
    while True:
        # Loop and wait for server commands
        while not busy:
            has_new_incoming = server.update_incoming()
            # TODO Change assumption that data only contains ID!!
            if has_new_incoming:
                print("bt_runner: has new incoming!")
                print("Data = ", server.incoming_data)
                cmd_type = bt_server_cmds.validate_cmd(server.incoming_data)
                print("Cmd id in runner-main: ", cmd_type)
                if cmd_type == "":
                    continue
                elif cmd_type == "rqst":
                    busy = True
                server.post_to_incoming()
                print("posted to incoming")
        print("bt_runner: waiting for outgoing")

        has_new_outgoing = server.update_outgoing()
        if (has_new_outgoing):
            print("bt_runner: sending data")
            server.send_data()
            busy = False


main()
