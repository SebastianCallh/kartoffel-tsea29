import bluetooth
import bt_task_handler


class BT_Server:
    """Create the server socket with predefined port and backlog value
       Returns a BluetoothSocket"""

    def __init__(self, server_addr, port, backlog, client_addr=""):
        # Sever bluetooth mac-address
        self.server_addr = server_addr
        self.port = port
        # Number of unaccepted connections before refusing new ones
        self.backlog = backlog
        # (the only address from which the server will accept connections)
        self.client_addr = client_addr

        # Set up server socket
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.setblocking(True)
        self.server_sock.bind((server_addr, port))
        # Enable the server to accept connections
        self.server_sock.listen(backlog)

        # Data received from client
        self.incoming_data = None
        # Data to be sent to client
        self.outgoing_data = None

        self.client_sock = None
        self.accp_client_addr = None

    def accept_connection(self):
        # TODO: Accept connection from valid client (requires change of backlog)
        print("in accept_connection")
        (self.client_sock, self.accp_client_addr) = self.server_sock.accept()

    # if accp_client_addr == client_addr


    def post_to_incoming(self):
        print("Server: staring to post to incoming")
        bt_task_handler.post_incoming(bt_task_handler.BT_task(self.incoming_data, ""))
        print("Server done posting to incoming, returning to main")

    def send_data(self, data=None):
        print("Server: sending!")
        if not data:
            self.client_sock.send(self.outgoing_data)
        else:
            self.client_sock.send(data)
        print("Server: sent! Returning to main")

    def _pop_from_outgoing(self):
        return bt_task_handler.pop_outgoing()

    """Updates incoming_data. Returns true if data was updated,
       false otherwise"""

    def update_incoming(self):
        has_new_incoming = False
        try:
            self.client_sock.settimeout(0.1)
            data = self.client_sock.recv(1024).decode('utf-8')
            print("bt_server: Data =", data)
            if len(data) != 0:  # TODO or None? (using json)
                self.incoming_data = data
                has_new_incoming = True
        except bluetooth.btcommon.BluetoothError:
            pass
        finally:
            self.client_sock.settimeout(None)
        return has_new_incoming

    """Updates outgoing_data. Returns true if data was updated,
       false otherwise"""

    def update_outgoing(self):
        has_new_outgoing = False
        task = self._pop_from_outgoing()
        # print("Updated outgoing task in server ", str(task))
        if type(task) == bt_task_handler.BT_task and task.cmd_id != 0:
            print("update_outgoing: i if-sats")
            self.outgoing_data = str(task.cmd_id) + ", " + str(task.data)  # TODO will change when json
            has_new_outgoing = True
        return has_new_outgoing

    def shutdown_server(self):
        #self.server_sock.shutdown(2)
        self.server_sock.close()
        self.client_sock.close()
