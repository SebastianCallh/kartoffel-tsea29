import bt_server
import bt_task_handler
import protocol

PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1
GOT_DATA = 1
NO_DATA = 0


def setup_server():
    server = bt_server.BT_Server(PI_ADDR, PORT, BACKLOG)
    #print("before accept_connection")
    server.accept_connection()
    #print("after accept_connection")
    bt_task_handler.clean_queue_files()
    return server


def validate_cmd(data):
    return True if data in protocol.BT_CLIENT_COMMANDS else False


def send(server):
    has_new_outgoing = server.update_outgoing()
    if (has_new_outgoing):
        #print("bt_runner: sending data")
        server.send_data()
    return has_new_outgoing


def recieve(server):
    has_new_incoming = server.update_incoming()
    # TODO Change assumption that data only contains ID!!

    if has_new_incoming:
        #print("Runner got new data")
        if int(server.incoming_data) == protocol.BT_SERVER_RESTART:
            #print("Runner got restart")
            return protocol.BT_SERVER_RESTART
        elif int(server.incoming_data) == protocol.BT_SERVER_SHUTDOWN:
            #print("Runner got shutdown")
            return protocol.BT_SERVER_SHUTDOWN
        else:
            #print("bt_runner: has new incoming!")
            #print("Data = " + server.incoming_data)
            server.post_to_incoming()
            #print("posted to incoming")
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
    while exit != protocol.BT_SERVER_SHUTDOWN:
        exit = recieve(server)
        send(server)
        if exit == protocol.BT_SERVER_RESTART or exit == protocol.BT_SERVER_SHUTDOWN:
            #print("Runner.main : exit == ", exit)
            has_sent = False
            while has_sent:
                has_sent = send(server)

            #print("Runner: server.client_sock =", server.client_sock)
            server.shutdown_server()
            del server
            #print("Runner: Deleted server and client sock")

            if exit == protocol.BT_SERVER_RESTART:
                server = setup_server()
                #print("Runner: NEW client_sock =", server.client_sock)
                exit = NO_DATA
                # Breaks if exit == SHUTDOWN


main()
