import bluetooth

client_addr = "00:15:83:2A:49:E4"
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 1
server_sock.bind(client_addr,port)
server_sock.listen(1)

client_sock,client_addr = server_sock.accept()
print("Accepted connection from %d \n", address)




server_sock.close()
	
	












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
