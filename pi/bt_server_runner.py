import bt_server
import bt_server_cmds
import bt_task_handler
import protocol

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1
EOF = -1
RESTART = 14
SHUTDOWN = 15
GOT_DATA = 1
NO_DATA = 0


def setup_server():
    server = bt_server.BT_Server(PI_ADDR, PORT, BACKLOG)
    print("before accept_connection")
    server.accept_connection()
    print("after accept_connection")
    bt_task_handler.clean_queue_files()
    return server

def validate_cmd(data):
    return True if data in protocol.BT_CLIENT_COMMANDS else False


def send(server):
    has_new_outgoing = server.update_outgoing()
    if (has_new_outgoing):
        print("bt_runner: sending data")
        server.send_data()
    return has_new_outgoing


def recieve(server):
    has_new_incoming = server.update_incoming()
    # TODO Change assumption that data only contains ID!!

    if has_new_incoming == bt_server.BT_EOF:
        return EOF
    elif has_new_incoming == bt_server.NEW_DATA:
        if int(server.incoming_data) == protocol.BT_SERVER_RESTART:
            return RESTART
        elif int(server.incoming_data) == protocol.BT_SERVER_SHUTDOWN:
            return SHUTDOWN
        else:
            print("bt_runner: has new incoming!")
            print("Data = " + server.incoming_data)
            server.post_to_incoming()
            print("posted to incoming")
            return GOT_DATA
    return NO_DATA


"""
  The main function initialize the server and runs it.
  The function handles the flow of information between
  the intermediary, server and client.
"""


def main():
    server = setup_server()
    exit = NO_DATA
    while exit != SHUTDOWN:
        exit = recieve(server)
        send(server)
        if exit == RESTART or exit == SHUTDOWN:
            has_sent = False
            while has_sent:
                has_sent = send(server)

            waiting = NO_DATA
            while waiting != EOF:
                waiting = recieve(server)

            server.shutdown_server()
            del server

            if exit == RESTART:
                server = setup_server()
                exit = 0
                # Breaks if exit == SHUTDOWN


main()
