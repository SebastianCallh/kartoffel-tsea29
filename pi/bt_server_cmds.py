import os

"""
File for miscellaneous functions.
Functions can be moved if no need of file otherwise.
"""


def get_pi_ip():
    """
    Returns IP address for Rasberry Pi connected to Eduroam.
    """
    s = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    pi_ip = s.read()
    return pi_ip
