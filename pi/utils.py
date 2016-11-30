"""
Various functions which does not belong in any other file.

NOTE: This file might have to be split if the list of functions grow too large.
"""
import os


# Returns the two's complementary value in it's python representation
def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val -= 1 << bits

    return val

    
def get_ip():
    s = os.popen('ifconfig wlan0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    pi_ip = s.read()
    return pi_ip