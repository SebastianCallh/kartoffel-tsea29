"""
Wrapper for the I2C bus with added functionality to support the packet protocol
the robot is using.
Packet protocol
----
I2C supports two functions for interacting on the bus:
  Read address,
  Write address
There functions are in turn addressed to specific slaves and contain the address
requested/set and a value when writing data. Each function write or read a
single byte.
As the desired functionality requires data to be sent and received in multi-byte
chunks this functionality must be abstracted away using a looser protocol. To
accomplish this the read and written addresses are purposely used incorrectly
to specify different states of receiving or sending data.
The protocol use two "addresses":
  PACKET_HEADER,
  PACKET_DATA
Using these two addresses it is possible to send data of the length 255 bytes by
first sending the data length and then all bytes in the data array until every
byte has been sent.
PACKET_HEADER:
Contains the length of the following data on the range 0 to 255. If there is no
data to be sent the value returned is 0.
PACKET_DATA:
Contains the data of the n:th read byte since the PACKET_HEADER. Reading data
from a packet which has already been read to the end has undefined behaviour.
The master-slave problem
----
As requests to read and write data can only be made from the master unit there
are difficulties actually notifying of new data from a slave unit. The protocol
solves this by reading the "addresses" periodically in order to search for
pending data. When data read from PACKET_HEADER is not zero there is data
available and the program can then read its data.
"""

import smbus

# Addresses for the units on the bus. Note that the laser cannot be queried
# using the protocol described above.
SENSOR_ADDR = 0x30
STYR_ADDR = 0x40
LASER_ADDR = 0x62

# Packet addresses
PACKET_HEADER = 0
PACKET_DATA = 1


class Bus:
    def __init__(self, interface=1):
        self.interface = interface
        self.bus = smbus.SMBus(1)

    def send(self, data, unit_addr):
        self._write_packet_start(len(data), unit_addr)
        self._write_packet_data(data, unit_addr)

    def try_receive(self, unit_addr):
		size = self._get_pending_packet_size(unit_addr)
		
		if size == 0:
			# No pending packet
			return None

		return self._read_packet_data(size, unit_addr)

    # Internal methods

    def _write_packet_start(self, packet_len, unit_addr):
        self.bus.write_byte_data(unit_addr, PACKET_HEADER, packet_len)

    def _write_packet_data(self, packet_data, unit_addr):
        for b in packet_data:
            self.bus.write_byte_data(unit_addr, PACKET_DATA, b)

    def _read_packet_data(self, packet_len, unit_addr):
        data = []
        for i in range(packet_len):
            data.append(self.bus.read_byte_data(unit_addr, PACKET_DATA))

        return data

    def _get_pending_packet_size(self, addr):
        return self.bus.read_byte_data(addr, PACKET_HEADER)