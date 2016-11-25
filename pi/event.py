"""
Container used to realize a command/event on the event bus and provides
functions for formatting the command as packet data.

See protocol.py for actual commands and their arguments.
"""
from command_processors import process_arguments

# Indexes of various data in received packets
ID_INDEX = 0
ARG_START_INDEX = 1


class Event:
    def __init__(self, message_id, arguments=None):
        self.message_id = message_id
        self.arguments = arguments or []

    @staticmethod
    def parse(data):
        return Event(data[ID_INDEX], data[ARG_START_INDEX:])

    def process(self):
        self.arguments = process_arguments(self.message_id, self.arguments)

    def as_packet_data(self):
        return [self.message_id] + self.arguments
