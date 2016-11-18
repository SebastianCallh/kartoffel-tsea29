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
        self.server_sock.bind((server_addr, port))
        # Enable the server to accept connections
        self.server_sock.listen(backlog)

        # Data received from client
        self.incoming_data = None
        # Data to be sent to client
        self.outgoing_data = None

        self.client_sock, self.accp_client_addr = None

    def accept_connection(self):
        # TODO: Accept connection from valid client (requires change of backlog)
        (self.client_sock, self.accp_client_addr) = self.server_sock.accept()

    # if accp_client_addr == client_addr


    def post_to_taskqueue(self):
        bt_task_handler.post(self.incoming_data)

    def send_data(self):
        self.client_sock.send(self.outgoing_data)

    def _pop_from_taskqueue(self):
        return bt_task_handler.pop()

    """Updates incoming_data. Returns true if data was updated,
       false otherwise"""

    def update_incoming(self):
        has_new_incoming = False
        data = self.client_sock.recv(1024)
        if len(data) != 0:  # TODO or None? (using json)
            incoming_data = data
            has_new_incoming = True
        return has_new_incoming

    """Updates outgoing_data. Returns true if data was updated,
       false otherwise"""

    def update_outgoing(self):
        has_new_outgoing = False
        (cmd_id, data) = self._pop_from_taskqueue()
        if len(data) != 0:
            outgoing_data = cmd_id + " " + data  # TODO will change when json
            has_new_outoing = True
        return has_new_outgoing
