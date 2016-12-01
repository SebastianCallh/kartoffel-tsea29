import bt_server
import bt_server_cmds
import bt_task_handler
import protocol

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1
GOT_DATA = 1
NO_DATA = 0


def setup_server():
    """
    Creates and returns a fresh bt_server connected to a client.
    """
    server = bt_server.BT_Server(PI_ADDR, PORT, BACKLOG)
    server.accept_connection()
    bt_task_handler.clean_queue_files()
    print("Server connected.")
    return server


def is_valid_cmd(command):
    """
    Checks if given command is a valid command from a client.
    Returns True/False.
    """
    return True if command in protocol.BT_CLIENT_COMMANDS else False


def send(server):
    """
    Sends data to client if given bt_server has new outgoing
    data from main unit.
    Returns True/False whether or not data was sent.
    """
    has_new_outgoing = server.update_outgoing()
    if (has_new_outgoing):
        server.send_data()
    return has_new_outgoing


def recieve(server):
    """
    Post incoming data to queue to main unit if given bt_server
    has new data.
    Returns NO_DATA, NEW_DATA, SHUTDOWN or RESTART depending on
    data from client.
    """
    has_new_incoming = server.update_incoming()
    # TODO Change assumption that data only contains ID!!

    if has_new_incoming:
        if int(server.incoming_data) == protocol.BT_SERVER_RESTART:
            return protocol.BT_SERVER_RESTART
        elif int(server.incoming_data) == protocol.BT_SERVER_SHUTDOWN:
            return protocol.BT_SERVER_SHUTDOWN
        else:
            server.post_to_incoming()
            return GOT_DATA
    return NO_DATA


def main():
    """
    The main function initializes instance of the server.
    Runs the main control of data flow in the bluetooth connection.
    """
    server = setup_server()
    exit = NO_DATA
    while exit != protocol.BT_SERVER_SHUTDOWN:
        exit = recieve(server)
        send(server)
        if exit == protocol.BT_SERVER_RESTART or exit == protocol.BT_SERVER_SHUTDOWN:
            has_sent = False
            while has_sent:
                has_sent = send(server)

            server.shutdown_server()
            del server

            if exit == protocol.BT_SERVER_RESTART:
                server = setup_server()
                exit = NO_DATA
                # Breaks if exit == SHUTDOWN


main()
