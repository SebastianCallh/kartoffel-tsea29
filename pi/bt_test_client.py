import bluetooth
import time

PI_ADDR = "B8:27:EB:FC:55:27"
USB_BT_ADDR = ""
PORT = 3


def setup_bt_client(addr, port):
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    if client_sock != None:
        print("Client_sock created, wow!")
    client_sock.setblocking(True)
    timeout = 10
    while timeout >= 0:
        try:
            client_sock.connect((addr, port))
            timeout = -1
        except bluetooth.btcommon.BluetoothError:
            time.sleep(1)
            timeout -= 1
            continue
    if timeout==0:
        print("Could not connect to server! PLZ try again and hope for better luck")
        return None
    else:     
        print("connected to ", addr)
        # client_sock.settimeout(1)
        return client_sock


def main():
    client_sock = setup_bt_client(PI_ADDR, PORT)
    if not client_sock:
        return

    while (True):
        print("Sock :", str(client_sock))
        msg = input("To server: ")

        if int(msg) == 14 or int(msg) == 15:
            print("Shutdown or restart")
            client_sock.send(msg)
            print("Has sent restart or shutdown")
            client_sock.shutdown(2)
            client_sock.close()
            print("Sent shutdown")
        else:
            print("Sock i else: ",str(client_sock))
            client_sock.send(msg)
        print("sent msg")

        data = ""

        try:
            while data == "":
                data = client_sock.recv(1024).decode('utf-8')
            if len(data) == 0:
                break
            print("received " + str(data))
        except bluetooth.btcommon.BluetoothError:
            print("Catching bluettoth error")
            # Recieved when server responds to shutdown
            client_sock.close()
            del client_sock
            if int(msg) == 14:
                print("Got msg == 14 in bluetoothError")
                # Restart requested
                client_sock = setup_bt_client(PI_ADDR, PORT)
            elif int(msg) == 15:
                # Shutdown requested
                print("Got msg == 15 in bluetoothError")
                break
        '''except IOError:
            print("Error = " + str(IOError))
        except OSError:
            print("Error = " + str(OSError))'''

    print("closed")


main()
