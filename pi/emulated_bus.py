import logging
from queue import Queue

from protocol import CMD_REQUEST_SENSOR_DATA, CMD_RETURN_SENSOR_DATA, STYR_ADDR, \
    SENSOR_ADDR, LASER_ADDR, PACKET_HEADER, PACKET_DATA

log = logging.getLogger(__name__)


class EmulatedBus:
    def __init__(self):
        self.slaves = {
            SENSOR_ADDR: EmulatedSlave(SENSOR_ADDR),
            STYR_ADDR: EmulatedSlave(STYR_ADDR),
            LASER_ADDR: EmulatedLaser
        }

    def write_byte_data(self, address, data_id, data):
        if address in self.slaves:
            self.slaves[address].write_byte_data(data_id, data)
        else:
            log.error('Trying to send data to nonexistant slave.')

    def read_byte_data(self, address, data_id):
        if address in self.slaves:
            return self.slaves[address].read_byte_data(data_id)
        else:
            log.error(
                'Trying to read data from nonexistant slave (address = {}).'
                .format(address)
            )
            return None


class EmulatedSlave:
    def __init__(self, address):
        self.address = address
        self.data_queue = Queue()

        # Receiving
        self.read_packet = None
        self.bytes_to_read = 0
        self.current_read_byte = 0

        # Transmitting
        self.transmitted_packet = None
        self.current_transmitted_byte = 0

    def write_byte_data(self, event_type, data):
        if event_type == PACKET_HEADER:
            if self.read_packet is not None:
                log.error(
                    'Data header incorrectly sent to address {} '
                    'which still waits for more bytes'
                    .format(self.address)
                )

            self.read_packet = []
            self.bytes_to_read = data
            self.current_read_byte = 0
        elif event_type == PACKET_DATA:
            if self.read_packet is None:
                log.error(
                    'Data incorrectly sent to address {} '
                    'without preceding packet header'
                    .format(self.address)
                )

            self.read_packet.append(data)
            self.current_read_byte += 1

            if self.current_read_byte >= self.bytes_to_read:
                if self.read_packet[0] == CMD_REQUEST_SENSOR_DATA:
                    self.data_queue.put([CMD_RETURN_SENSOR_DATA, 0, 0, 0, 0])

                self.read_packet = None

    def read_byte_data(self, data_id):
        if data_id == PACKET_HEADER:
            if self.transmitted_packet is not None:
                log.error(
                    'Data header incorrectly requested from address {} '
                    'which still sends bytes'
                    .format(self.address)
                )

            if self.data_queue.empty():
                return 0

            self.transmitted_packet = self.data_queue.get()
            self.current_transmitted_byte = 0

            return len(self.transmitted_packet)
        elif data_id == PACKET_DATA:
            if self.transmitted_packet is None:
                log.error(
                    'Data incorrectly requested from address {} '
                    'without preceding packet header'
                    .format(self.address)
                )

            data = self.transmitted_packet[self.current_transmitted_byte]
            self.current_transmitted_byte += 1

            if self.current_transmitted_byte >= len(self.transmitted_packet):
                self.transmitted_packet = None

            return data


class EmulatedLaser:
    def write_byte_data(self, *args):
        pass

    def read_byte_data(self, *args):
        return 0
