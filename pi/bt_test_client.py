import bluetooth

PI_ADDR = "B8:27:EB:FC:55:27"
USB_BT_ADDR = ""
port = 3

client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

print("Created client sock")
client_sock.connect((PI_ADDR,port))
print("connected to %s \n", PI_ADDR)
client_sock.settimeout(1)

while(True):
	#msg = input("To server: ")

	#client_sock.send(msg)
	#print("sent msg")

	data = ""

	try:
		while data == "":
			data = client_sock.recv(1024)
		if len(data) == 0:
		    break
		print("received " + str(data))
		time.sleep(3)
	except IOError:
		print("Error = " + str(IOError))
		pass



client_sock.close()
print("closed")
