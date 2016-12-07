import bt_server
import bt_task_handler
import protocol
import utils

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1
GOT_DATA = 1
NO_DATA = 0


def setup_server():
    """
    Creates and returns a fresh bt_server connected to a client.
    """
    bt_task_handler.clean_queue_files()
    server = bt_server.BT_Server(PI_ADDR, PORT, BACKLOG)
    server.accept_connection()

    print("Server connected.")
    return server


def is_valid_cmd(command):
    """
    Checks if given command is a valid command from a client.
    Returns True/False.
    """
    return True if command in protocol.BT_CLIENT_COMMANDS else False


def send(server, data=None):
    """
    Sends data to client if given bt_server has new outgoing
    data from main unit.
    Returns True/False whether or not data was sent.
    """
    if not data:
        has_new_outgoing = server.update_outgoing()
        if has_new_outgoing:
            server.send_data()
        return has_new_outgoing
    else:
        server.send_data(data)
        has_new_outgoing = True
        return has_new_outgoing


def recieve(server):
    """
    Post incoming data to queue to main unit if given bt_server
    has new data.
    Returns NO_DATA, NEW_DATA, SHUTDOWN or RESTART depending on
    data from client.
    """
    has_new_incoming = server.update_incoming()

    if has_new_incoming:
        if int(server.incoming_data) == protocol.BT_SERVER_RESTART:
            return protocol.BT_SERVER_RESTART
        elif int(server.incoming_data) == protocol.BT_SERVER_SHUTDOWN:
            return protocol.BT_SERVER_SHUTDOWN
        elif int(server.update_incoming) == protocol.REQUEST_PI_IP:
            # Return ip immediately without passing on to task_handler
            return protocol.REQUEST_PI_IP
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
    status = NO_DATA
    while exit != protocol.BT_SERVER_SHUTDOWN:
        status = recieve(server)
        if status == protocol.REQUEST_PI_IP:
            send([utils.get_ip()])
        else:
            send(server)
        if status == protocol.BT_SERVER_RESTART or status == protocol.BT_SERVER_SHUTDOWN:
            has_sent = False
            while has_sent:
                has_sent = send(server)

            server.shutdown_server()
            del server

            if status == protocol.BT_SERVER_RESTART:
                server = setup_server()
                status = NO_DATA
                # Breaks if exit == SHUTDOWN


main()
