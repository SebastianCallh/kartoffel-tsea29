import bluetooth

PI_ADDR = "B8:27:EB:FC:55:27"
client_addr = ""

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 3
server_sock.bind((PI_ADDR, port))
server_sock.listen(1)

print("Init performed")

(client_sock, client_addr) = server_sock.accept()
print("Accepted connection from %s \n", client_addr)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0:
            break
        print("received [%s]" % data)
except IOError:
    pass


server_sock.close()
print("Closed")













'''import socket

hostMACAddress = '00:15:83:2A:49:E4' # The MAC address of a Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 3 # 3 is an arbitrary choice. However, it must match the port used by the client.
backlog = 1
size = 1024
s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
s.bind((hostMACAddress,port))
s.listen(backlog)
try:
    client, address = s.accept()
    while 1:
        data = client.recv(size)
        if data:
            print(data)
            client.send(data)
except:	
    print("Closing socket")	
    client.close()
    s.close()'''
