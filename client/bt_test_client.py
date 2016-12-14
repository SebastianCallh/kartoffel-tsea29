import bluetooth
import time
import traceback
import protocol

PI_ADDR = "B8:27:EB:FC:55:27"
USB_BT_ADDR = ""
PORT = 3


def setup_bt_client(addr, port):
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_sock.setblocking(True)
    timeout = 10
    while timeout > 0:
        try:
            client_sock.connect((addr, port))
            timeout = -1
        except bluetooth.btcommon.BluetoothError:
            time.sleep(1)
            timeout -= 1
            print("Waiting for connection...")
            continue

    if timeout == 0:
        print("Could not connect to server! PLZ try again and hope for better luck")
        return client_sock
    else:
        print("Successfully connected to ", addr)
        return client_sock


def main():
    restart = ""
    while not restart == "EXIT":
        restart = run()
        time.sleep(1)


def run():
    client_sock = setup_bt_client(PI_ADDR, PORT)

    while (True):
        msg = input("To server: ")

        client_sock.send(msg)

        data = ""

        try:
            while data == "":
                data = client_sock.recv(1024).decode('utf-8')
            if len(data) == 0:
                break
        except bluetooth.btcommon.BluetoothError:
            # Recieved when server responds to shutdown
            client_sock.close()
            del client_sock
            if int(msg) == protocol.BT_SERVER_RESTART:
                # Restart requested
                return "RESTART"
            elif int(msg) == protocol.BT_SERVER_SHUTDOWN:
                # Shutdown requested
                return "EXIT"


main()
