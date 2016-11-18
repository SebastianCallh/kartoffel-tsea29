import bt_server
import bt_utility


PI_ADDR = "B8:27:EB:FC:55:27"
PORT = 3
BACKLOG = 1




"""
  The main function initialize the server and runs it. 
  The function handles the flow of information between
  the intermediary, server and client. 
"""
def main():
	
	busy = False
	
	server_sock = init()
	server = BT_Server(PI_ADDR, PORT, BACKLOG)
	
	server.accept_connection()
	
	#TODO add exit/restart options (conditions in loop)
	while(True):
		# Loop and wait for server commands
		while(not busy):
			has_new_incoming = server.update_incoming()
			#TODO Change assumption that data only contains ID!! 
			cmd_type = bt_utility.validate_cmd(BT_server.incoming_data)
			if(cmd_type == ""):
				continue
			elif(cmd_type == "rqst"):
				busy = True
			if(has_new_incoming):
				post_to_taskqueue()
		has_new_outgoing = update_outgoing()
		if(has_new_outgoing):
			send_data()
			busy = False





main()


