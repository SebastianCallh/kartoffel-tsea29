import outbound
from observer import Observer

observer_map = {x: Observer() for x in range(1, outbound.NUM_CMDS + 1)}


def read_messages(bus):
    while True:
        msg = bus.try_receive()
        if msg is None:
            return

        packet_id = msg[0]
        if packet_id in observer_map:
            observer_map[packet_id].notify(msg)
        else:
            print('Unknown packet id: ' + packet_id)


def subscribe_to_cmd(cmd, func):
    if cmd in observer_map:
        observer_map[cmd].subscribe(func)
    else:
        print('Trying to subscribe to unknown cmd')
