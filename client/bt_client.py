import bluetooth
import time
import traceback
import threading
import queue
import protocol
from bt_task import BT_task
from ast import literal_eval


class BT_client(threading.Thread):
    PI_ADDR = "B8:27:EB:FC:55:27"
    PORT = 3

    def __init__(self, queue_handler):
        self.queue_handler = queue_handler
        self.exit_demanded = False
        self.restart_demanded = False
        self.client_sock = None
        threading.Thread.__init__(self)
        self.daemon = True
        self.is_connected = False


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
                print("Successfully connected to ", self.PI_ADDR)
                timeout = -1
            except bluetooth.btcommon.BluetoothError:
                time.sleep(1)
                timeout -= 1
                print("Waiting for connection...")
                continue
            except OSError:
                time.sleep(1)
                timeout -= 1
                print("OSError in _setup_bt_client (waiting connection)")
                continue

        if timeout == 0:
            print("Connection timeout. Could not connect to server!")
            return None
        else:
            print("Connected to ", self.PI_ADDR)
            self.is_connected = True

            return self.client_sock

    '''
         Loops send(),_recieve() until a shutdown or exit command is issued
         '''

    def _start_bt_client(self):
        self.client_sock = self._setup_bt_client()

        if self.client_sock:
            while True:
                self._send()
                status = self._receive()
                if status != "":
                    return status
        else:
            print("Could not connect to server, no socket created")

    def _send(self):
        bt_out_task = self.queue_handler.pop_out_queue()
        if bt_out_task:
            self.current_out_task = bt_out_task
            try:
                self.client_sock.send(str(bt_out_task.cmd_id))
            except bluetooth.btcommon.BluetoothError:
                pass
            except OSError:
                pass
                
            if bt_out_task.cmd_id == protocol.BT_SERVER_SHUTDOWN:
                self.exit_demanded = True
            elif bt_out_task.cmd_id == protocol.BT_SERVER_RESTART:
                self.restart_demanded = True
        else:
            self.current_out_task = BT_task(0, 0)
        

    def _receive(self):
        # Wait for incoming messages for 0.1 seconds
        recv_timeout = 0.1  # Receive timeout 0.1 seconds
        data = ""
        self.client_sock.settimeout(recv_timeout)
        try:
            data = self.client_sock.recv(1024).decode('utf-8')
        except bluetooth.btcommon.BluetoothError:
            # Recieved when server responds to shutdown
            pass
        except OSError:
            pass
        self.client_sock.settimeout(0)

        if self.restart_demanded:
            # Restart requested
            self.client_sock.close()
            del self.client_sock
            return "RESTART"
        elif self.exit_demanded:
            # Shutdown requested
            self.client_sock.close()
            del self.client_sock
            return "EXIT"

        if data:
            data = literal_eval(data)
            bt_in_task = BT_task(data[0], data[1])

            self.queue_handler.post_in_queue(bt_in_task)
            print("Bt client received: ", str(data[1]))

        return ""

    '''
    Overriden run()-method form threading.Thread.
    Updates client until a shutdown command is
    issued.
    '''

    def run(self):
        status = ""
        while not status == "EXIT":
            self.restart_demanded = False
            self.exit_demanded = False
            status = self._start_bt_client()
            if status == "ERROR":
                # TODO Add a task to out_queue
                print("A Bluetooth error occurred!")
            # Sleep so server has time to restart
            time.sleep(2)
