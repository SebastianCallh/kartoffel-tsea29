import bluetooth
import time
import traceback

PI_ADDR = "B8:27:EB:FC:55:27"
USB_BT_ADDR = ""
PORT = 3


def setup_bt_client(addr, port):
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print("Sock :", str(client_sock))
    client_sock.setblocking(True)
    timeout = 10
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
        
    if timeout==0:
        print("Could not connect to server! PLZ try again and hope for better luck")
        return client_sock
    else:     
        print("connected to ", addr)
        # client_sock.settimeout(1)
        return client_sock


def main():
    restart = ""
    while not restart == "EXIT":
        restart = run()
        time.sleep(1)




def run():
    client_sock = setup_bt_client(PI_ADDR,PORT)

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
        except bluetooth.btcommon.BluetoothError:
            print("Catching bluettoth error")
            # Recieved when server responds to shutdown
            #client_sock.shutdown(2)
            client_sock.close()
            del client_sock
            if int(msg) == 14:
                print("Got msg == 14 in bluetoothError")
                # Restart requested
                #print("Sock after restart: ",str(client_sock))
                return "RESTART"
            elif int(msg) == 15:
                # Shutdown requested
                print("Got msg == 15 in bluetoothError")
                return "EXIT"


main()
