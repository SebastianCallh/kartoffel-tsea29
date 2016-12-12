import bluetooth
import bt_task_handler
from bt_task import BT_task


class BT_Server:
    """
    Class for handling the Bluetooth connection to a client.
    Gives an interface for sending and receiving data between
    robot and client.
    """

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
        """
        Connects the server to the client trying to connect.
        """
        # TODO: Accept connection from valid client (requires change of backlog)
        (self.client_sock, self.accp_client_addr) = self.server_sock.accept()
        print("Connected")

    def post_to_incoming(self):
        """
        Puts saved incoming data to queue to robot.
        """
        bt_task_handler.post_incoming(BT_task(self.incoming_data, ""))

    def send_data(self, data=None):
        """
        Sends data via bluetooth to connected client.
        Sends data saved in server, unless data is passed.
        """
        if data:
            self.outgoing_data = str(data.cmd_id) + ", " + str(data.data)
        self.client_sock.send(self.outgoing_data)

    def _pop_from_outgoing(self):
        return bt_task_handler.pop_outgoing()

    def update_incoming(self):
        """
        Updates incoming data aimed for the robot by receiving via bluetooth.
        Saves the new data in itself.
        Returns True/False whether or not new data was received.
        """
        has_new_incoming = False
        try:
            self.client_sock.settimeout(0.1)
            data = self.client_sock.recv(1024).decode('utf-8')
            if len(data) != 0:  # TODO or None? (using json)
                self.incoming_data = data
                has_new_incoming = True
        except bluetooth.btcommon.BluetoothError:
            pass
        finally:
            self.client_sock.settimeout(None)
        return has_new_incoming

    def update_outgoing(self):
        """
        Updates outgoing_data aimed for client by poping from robots queue.
        Saves the new data in itself.
        Returns true if data was updated, false otherwise
        """
        has_new_outgoing = False
        task = self._pop_from_outgoing()
        if type(task) == BT_task and task.cmd_id != 0:
            self.outgoing_data = str(task.cmd_id) + ", " + str(task.data)
            has_new_outgoing = True
        return has_new_outgoing

    def shutdown_server(self):
        """
        Shuts down itself by closing server and client sockets.
        """
        self.server_sock.shutdown(2)
        self.server_sock.close()
        self.client_sock.close()
        print("Closed connection.")
