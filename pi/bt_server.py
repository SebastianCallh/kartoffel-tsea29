import bluetooth
import bt_task_handler


class BT_Server:


	# Server bluetooth address
	server_addr = ""
	# Client address
	# (the only address from which the server will accept connections)
	client_addr = ""
	port = 0
	# Number of unaccepted connections before refusing new ones
	backlog = 0


	server_sock = None
	(client_sock,accp_client_addr) = (None,None)
	
	# Data received from client
	incoming_data = None
	# Data to be sent to client
	outgoing_data = None
	
	intermediary = bt_server_intermediary.BT_Intermediary()
	
	"""Create the server socket with predefined port and backlog value
	   Returns a BluetoothSocket"""
	def __init__(self, server_addr, port, backlog, client_addr=""):
		server_addr = server_addr
		port = port
		backlog = backlog
		client_addr = client_addr
		
		# Set up server socket
		server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
		server_sock.bind((server_addr, port))
		# Enable the server to accept connections
		server_sock.listen(backlog)
		
	def accept_connection():
		# TODO: Accept connection from valid client (requires change of backlog)
		(client_sock, accp_client_addr) = server_sock.accept()
		#if accp_client_addr == client_addr
	
		
	def post_to_taskqueue():
		bt_task_handler.post()
	
	def send_data():
		client_sock.send(outgoing_data)
		
	def _pop_from_taskqueue():
		return bt_task_handler.pop()
	
	"""Updates incoming_data. Returns true if data was updated, 
	   false otherwise"""			
	def update_incoming():
		has_new_incoming = False
		data = client_sock.recv(1024)
		if len(data) != 0:                   		#TODO or None? (using json)
			incoming_data = data
			has_new_incoming = True
		return has_new_incoming
	
	"""Updates outgoing_data. Returns true if data was updated, 
	   false otherwise"""			
	def update_outgoing():
		has_new_outoing = False
		(cmd_id,data) = _pop_from_taskqueue()
		if len(data) != 0:
			outgoing_data = cmd_id + " " + data     #TODO will change when json
			has_new_outoing = True
		return has_new_outgoing
	







	
