import bluetooth
import time
import traceback
import protocol
import threading



class BT_client(threading.Thread):
    PI_ADDR = "B8:27:EB:FC:55:27"
    USB_BT_ADDR = ""
    PORT = 3
    
    '''
    Creates a new client sock and attempts to connect to
    addr via port. Timeout can be specified, default value is
    10 seconds. The created socket is returned if connection
    was succesful, else return None.
    '''
    def setup_bt_client(addr,port,timeout=10):
        client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        client_sock.setblocking(True)
        
        while timeout > 0:
            try:
                client_sock.connect((addr, port))
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
            print("connected to ", addr)
            return client_sock


    def __init__(self, in_queue, out_queue):
        self.client_sock = setup_bt_client(PI_ADDR,PORT)      
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue

    '''
    Overriden run()-method form threading.Thread.
    Updates client until a shutdown command is 
    issued.
    '''
    def run(self):
        status = ""
        while not status == "EXIT":
            status = update(self)
            if status == "ERROR":
                #TODO Add a task to out_queue
                print("A bluetooth error occured!")
            # Sleep so server has time to restart
            time.sleep(1)
    
    '''
    Loops recieve(),send() until a shutdown or exit command is issued
    '''
    def update(self):
        recv_timeout = 0.1             # Recieve timeout 0.1 seconds
        client_sock = setup_bt_client(PI_ADDR, PORT)

        while (True):
            try:
                # Try to get task from queue
                # Blocking set to false
                bt_task = self.out_queue.get(False)
            except Empty:
                # No task avaiable
                pass

            #TODO Possible fix! Concantenate cmd_id and data
            try:
                client_sock.send(str(bt_task.id))
            except bluetooth.btcommon.BluetoothError:
                print(traceback.format_exc())
                
            print("sent msg")
               
            # Wait for incoming messages for 0.1 seconds
            client_sock.settimeout(recv_timeout)
            try:
                data = client_sock.recv(1024).decode('utf-8')
                print("received " + str(data))
            except bluetooth.btcommon.BluetoothError:                
                # Recieved when server responds to shutdown
                print("Catching bluetooth error")
                # Destroy client socket
                client_sock.close()
                del client_sock
                
                if int(msg) == protocol.BT_SERVER_RESTART:
                    print("Got restart in bluetoothError")
                    # Restart requested
                    return "RESTART"
                elif int(msg) == protocol.BT_SERVER_SHUTDOWN:
                    # Shutdown requested
                    print("Got msg exit in bluetoothError")
                    return "EXIT"
                else:
                    return "ERROR"
            finally:
                client_sock.settimeout(None)
