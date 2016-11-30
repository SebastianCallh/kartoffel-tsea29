import bluetooth
import time
import traceback
import threading
import queue
import protocol
from bt_task import BT_task


class BT_client(threading.Thread):
    PI_ADDR = "B8:27:EB:FC:55:27"
    PORT = 3

    def __init__(self, queue_handler):
        self.queue_handler = queue_handler
        self.current_out_task = None
        self.client_sock = None
        threading.Thread.__init__(self)

    '''
    Creates a new client sock and attempts to connect to
    addr via port. Timeout can be specified, default value is
    10 seconds. The created socket is returned if connection
    was succesful, else return None.
    '''

    def _setup_bt_client(self, timeout=10):
        self.client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_sock.setblocking(True)

        while timeout > 0:
            try:
                self.client_sock.connect((self.PI_ADDR, self.PORT))
                timeout = -1
            except bluetooth.btcommon.BluetoothError:
                time.sleep(1)
                timeout -= 1
                print("waiting for connection...")
                print(traceback.format_exc())
                continue

        if timeout == 0:
            print("Connection timeout. Could not connect to server!")
            return None
        else:
            print("connected to ", self.PI_ADDR)
            return self.client_sock

    '''
         Loops send(),_recieve() until a shutdown or exit command is issued
         '''

    def _start_bt_client(self):
        self.client_sock = self._setup_bt_client()

        while (True):
            self._send()
            status = self._receive()
            if status != "":
                return status

    def _send(self):
        bt_out_task = self.queue_handler.pop_out_queue()
        self.current_out_task = bt_out_task

        # TODO Possible fix! Concatenate cmd_id and data
        try:
            self.client_sock.send(str(bt_out_task.id))
        except bluetooth.btcommon.BluetoothError:
            print(traceback.format_exc())

        print("sent msg")

    def _receive(self):
        # Wait for incoming messages for 0.1 seconds
        recv_timeout = 0.1  # Receive timeout 0.1 seconds
        self.client_sock.settimeout(recv_timeout)
        try:
            data = self.client_sock.recv(1024).decode('utf-8')
            print("received " + str(data))
        except bluetooth.btcommon.BluetoothError:
            # Recieved when server responds to shutdown
            print("Catching bluetooth error")
            # Destroy client socket
            self.client_sock.close()
            del self.client_sock

            if int(self.current_out_task.cmd_id) == protocol.BT_SERVER_RESTART:
                print("Bt client restart")
                # Restart requested
                return "RESTART"
            elif int(self.current_out_task.cmd_id) == protocol.BT_SERVER_SHUTDOWN:
                # Shutdown requested
                print("Bt client exit")
                return "EXIT"
            else:
                return "ERROR"
        finally:
            self.client_sock.settimeout(None)

        data_items = data.split(', ')
        bt_in_task = BT_task(data_items[0], data_items[1:])

        self.queue_handler.post_in_queue(bt_in_task)

        return ""

    '''
    Overriden run()-method form threading.Thread.
    Updates client until a shutdown command is
    issued.
    '''

    def run(self):
        status = ""
        while not status == "EXIT":
            status = self._start_bt_client()
            if status == "ERROR":
                # TODO Add a task to out_queue
                print("A bluetooth error occured!")
            # Sleep so server has time to restart
            time.sleep(1)
