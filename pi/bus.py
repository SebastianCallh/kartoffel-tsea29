import smbus

PACKET_HEADER = 0
PACKET_DATA = 1


class Bus:
    def __init__(self, default_addr=0x30, interface=1):
        self.default_addr = default_addr
        self.interface = interface
        self.bus = smbus.SMBus(1)

    def send(self, data, addr=None):
        if addr is None:
            addr = self.default_addr

        self._write_packet_start(len(data), addr)
        self._write_packet_data(data, addr)

    def try_receive(self, addr=None):
        if addr is None:
            addr = self.default_addr

        size = self._get_pending_packet_size(addr)
        if size == 0:
            # No pending packet
            return None

        return self._read_packet_data(size, addr)

    def _write_packet_start(self, packet_len, addr):
        self.bus.write_byte_data(addr, PACKET_HEADER, packet_len)

    def _write_packet_data(self, packet_data, addr):
        for b in packet_data:
            self.bus.write_byte_data(addr, PACKET_DATA, b)

    def _read_packet_data(self, packet_len, addr):
        data = []
        for i in range(packet_len):
            data.append(self.bus.read_byte_data(addr, PACKET_DATA))

    def _get_pending_packet_size(self, addr):
        return self.bus.read_byte_data(addr, PACKET_HEADER)
