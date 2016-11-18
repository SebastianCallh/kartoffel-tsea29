import protocol
import os



def validate_cmd(cmd_id):
	if(cmd_id in protocol.DATA_REQUESTS):
		return "rqst"
	elif(cmd_id in protocol.DIRECT_OPERATIONS):
		return "direct"
	else:
		return ""
		
		
def get_pi_ip():
	s = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | 				cut -d" " -f1')
	pi_ip = s.read()
	return pi_ip
