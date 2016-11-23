import bluetooth
import time

PI_ADDR = "B8:27:EB:FC:55:27"
USB_BT_ADDR = ""
PORT = 3


def setup_bt_client(addr, port):
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    if client_sock != None:
        print("Client_sock created, wow!")
    client_sock.connect((addr, port))
    print("connected to ", addr)
    client_sock.setblocking(True)
    # client_sock.settimeout(1)
    return client_sock


def main():
    client_sock = setup_bt_client(PI_ADDR, PORT)

    while (True):
        msg = input("To server: ")

        client_sock.send(msg)
        print("sent msg")

        data = ""

        try:
            while data == "":
                data = client_sock.recv(1024).decode('utf-8')
            if len(data) == 0:
                break
            print("received " + str(data))
        except EOFError:
            # Recieved when server responds to shutdown
            client_sock.close()
            del client_sock
            if int(msg) == 14:
                # Restart requested
                client_sock = setup_bt_client(PI_ADDR, PORT)
            elif int(msg) == 15:
                # Shutdown requested
                break
        except IOError:
            print("Error = " + str(IOError))
        except OSError:
            print("Error = " + str(OSError))


    print("closed")


main()
