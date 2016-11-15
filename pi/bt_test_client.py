import bluetooth

server_addr = "B8:27:EB:FC:55:27"
port = 50000
client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print("created client_sock")
client_sock.connect((server_addr,port))
print("connected to %d \n", server_addr)

client_sock.send("Kartoffel paj")
print("sent msg")




sock.close()













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
