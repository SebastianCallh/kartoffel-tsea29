"""
Distributed event bus which is shared between all units on the main bus and via
Bluetooth.

The event bus provides a way to send data back and forth between different
units on the I2C bus and via Bluetooth by applying asynchronous transmission of
all events, it is therefore not guaranteed that messages are received on the
other end. As not all commands must be subscribed to it is also not certain
that the receiving unit actually reacts on the commands it receive.

In order for the event bus to function both ways the bus must be manually
polled for incoming messages by calling EventBus.receive(). This will read
pending commands from all connected AVR units and then call their respective
handlers if the command has been subscribed to.

Supported commands and their arguments are defined in protocol.py.
"""

from observer import Observer
import bt_task_handler

from protocol import BLUETOOTH_ADDR

# As reading from the bus is a blocking operation it might cause actual program
# code to execute too late if there are many pending commands available. In
# order to prevent the read operation to consume too much time the amount of
# messages read each iteration is limited.

MAX_READ_COUNT = 10


class EventBus:
    observers = {}

    @staticmethod
    def post(addr, message):
        bt_task_handler.post_outgoing(message)

    @staticmethod
    def pop(unit_addr):
        return bt_task_handler.pop_incoming()  # bluetooth pop()

    @staticmethod
    def receive():
        EventBus.receive_from_addr(BLUETOOTH_ADDR)

    @staticmethod
    def receive_from_addr(unit_addr):
        for i in range(MAX_READ_COUNT):
            data = EventBus.pop(unit_addr)
            if data is None:
                break

            EventBus.notify(data.cmd_id, *data.data)

    @staticmethod
    def subscribe(command_id, handler):
        observer = EventBus._get_observer_for_command(command_id)
        observer.subscribe(handler)

    @staticmethod
    def notify(command_id, *args):
        observer = EventBus._get_observer_for_command(command_id)
        observer.notify(*args)

    @staticmethod
    def _get_observer_for_command(command_id):
        if command_id not in EventBus.observers:
            EventBus.observers[command_id] = Observer()

        return EventBus.observers[command_id]
