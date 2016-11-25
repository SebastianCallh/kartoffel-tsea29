import protocol
import os


def get_pi_ip():
    s = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    pi_ip = s.read()
    return pi_ip
    
def test_rqst():
    return "hej"

