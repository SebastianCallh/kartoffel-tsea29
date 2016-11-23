import bluetooth
import time

PI_ADDR = "B8:27:EB:FC:55:27"
USB_BT_ADDR = ""
PORT = 3


def setup_bt_client(addr, port):
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print("Created client sock")
    client_sock.connect((addr, port))
    print("connected to ", addr)
    client_sock.setblocking(True)
    # client_sock.settimeout(1)
    return client_sock


def main():
    client_sock = setup_bt_client(PI_ADDR, PORT)

    while (True):
        global client_sock
        msg = input("To server: ")

        client_sock.send(msg)
        print("sent msg")

        if int(msg) == 14:
            debug_count = 0
            while True:
                debug_count += 1
                try:
                    if debug_count % 100 == 0:
                        print("Top of try")
                    if client_sock != None:
                        print("Client_sock exsist, wow!")
                    client_sock.close()
                    del client_sock
                    client_sock = setup_bt_client(PI_ADDR, PORT)
                    print("restarting")
                    break
                except bluetooth.btcommon.BluetoothError:
                    if debug_count % 1000 == 0:
                        print("Error = ", bluetooth.btcommon.BluetoothError)
                    continue
            continue
        elif int(msg) == 15:
            print("Exiting")
            client_sock.close()
            break

        data = ""

        try:
            while data == "":
                data = client_sock.recv(1024).decode('utf-8')
            if len(data) == 0:
                break
            print("received " + str(data))
        except IOError:
            print("Error = " + str(IOError))
        except OSError:
            print("Error = " + str(OSError))

    print("closed")


main()
