import bluetooth

PI_ADDR = "B8:27:EB:FC:55:27"
port = 3

client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

print("Created client sock")
client_sock.connect((PI_ADDR,port))
print("connected to %s \n", PI_ADDR)

client_sock.send("Kartoffel paj")
print("sent msg")




client_sock.close()
print("closed")













'''import socket

serverMACAddress = 'B8:27:EB:FC:55:27'
port = 3
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.connect((serverMACAddress,port))
while 1:
    text = input()
    if text == "quit":
        break
    s.send(bytes(text, 'UTF-8'))
s.close()'''
