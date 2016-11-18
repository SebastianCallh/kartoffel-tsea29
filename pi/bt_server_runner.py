import bt_server
import bt_server_cmds

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

    server.accept_connection()

    # TODO add exit/restart options (conditions in loop)
    while True:
        # Loop and wait for server commands
        while not busy:
            has_new_incoming = server.update_incoming()
            # TODO Change assumption that data only contains ID!!
            if has_new_incoming:
                cmd_type = bt_server_cmds.validate_cmd(server.incoming_data)
                if cmd_type == "":
                    continue
                elif cmd_type == "rqst":
                    busy = True
                server.post_to_taskqueue()

        has_new_outgoing = server.update_outgoing()
        if (has_new_outgoing):
            server.send_data()
            busy = False

main()
