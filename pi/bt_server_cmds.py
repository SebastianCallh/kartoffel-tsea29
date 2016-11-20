import protocol
import os


def validate_cmd(cmd_id):
    if (int(cmd_id) in protocol.DATA_REQUESTS):
        print("command is a request")
        return "rqst"
    elif (int(cmd_id) in protocol.DIRECT_OPERATIONS):
        return "direct"
    else:
        return ""


def get_pi_ip():
    s = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    pi_ip = s.read()
    return pi_ip

