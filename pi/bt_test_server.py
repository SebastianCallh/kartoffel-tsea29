import bluetooth
import os
import time



time.sleep(20)

f = open('log.txt', 'w')
f.write('start')

PI_ADDR = "B8:27:EB:FC:55:27"
client_addr = ""

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

port = 3
server_sock.bind((PI_ADDR, port))
server_sock.listen(1)


f.write('Init perfomed\n')
#print("Init performed")

(client_sock, client_addr) = server_sock.accept()
#print("Accepted connection from %s \n", client_addr)
f.write("Accepted connection from %s \n" + str(client_addr) + '\n')

data = ""

try:
    while data == "":
        f.write('getting data\n')
        # print("getting data")
        data = client_sock.recv(1024)
        if len(data) == 0:
            break
        # print("received " + str(data))
        f.write('Recieved ' + str(data) + '\n')
except IOError:
    # print("Error = " + str(IOError))
    f.write('Error = ' + str(IOError) + '\n')
    pass

f1 = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
pi_ip = f1.read()
#print("Reading ip: " + str(pi_ip))
f.write('Reading ip: ' + str(pi_ip) + '\n')

try:
    # print("Sending IP")
    f.write('Sending IP\n')
    client_sock.send("IP address: " + str(pi_ip))
    # print("IP sent")
    f.write('IP sent\n')
except IOError:
    # print("Error = " + str(IOError))
    f.write('Error = ' + str(IOError) + '\n')


server_sock.close()
# print("Closed")
f.write('Closed\n')

f.close()










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
