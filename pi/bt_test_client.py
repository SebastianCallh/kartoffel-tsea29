import bluetooth
import time

PI_ADDR = "B8:27:EB:FC:55:27"
USB_BT_ADDR = ""
port = 3

client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

print("Created client sock")
client_sock.connect((PI_ADDR, port))
print("connected to ", PI_ADDR)
client_sock.setblocking(True)
#client_sock.settimeout(1)

while (True):
    msg = input("To server: ")

    client_sock.send(msg)
    print("sent msg")
    
    if msg == 14:
        client_sock.connect((PI_ADDR,port))
        client_sock.setblocking(True)
        continue
    elif msg == 15:
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
