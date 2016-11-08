import outbound
from observer import Observer

raw_observer_map = {x: Observer() for x in range(1, outbound.NUM_CMDS + 1)}
observer_map = {x: Observer() for x in range(1, outbound.NUM_CMDS + 1)}


def register_map(cmd, func):
    raw_observer_map[cmd].subscribe(lambda msg: observer_map[cmd].notify(*func(msg)))


def read_messages(bus):
    while True:
        msg = bus.try_receive()
        if msg is None:
            return

        packet_id = msg[0]
        if packet_id in raw_observer_map:
            raw_observer_map[packet_id].notify(msg)
        else:
            print('Unknown packet id: ' + packet_id)


def subscribe_to_cmd(cmd, func):
    if cmd in observer_map:
        observer_map[cmd].subscribe(func)
    else:
        print('Trying to subscribe to unknown cmd')


register_map(outbound.CMD_RETURN_SENSOR_DATA, lambda msg: [msg[1], msg[2]])
