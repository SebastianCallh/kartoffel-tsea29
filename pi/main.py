from datetime import datetime, timedelta

from bus import Bus
from messages import read_messages, subscribe_to_cmd
from outbound import request_sensor_data, CMD_RETURN_SENSOR_DATA

bus = Bus()

last_request = datetime.now()
request_period = timedelta(seconds=2)


def sensor_data_received(msg):
    ir_left_mm = msg[1]
    ir_right_mm = msg[2]

    print('ir_left_mm: ' + ir_left_mm)
    print('ir_right_mm: ' + ir_right_mm)


subscribe_to_cmd(CMD_RETURN_SENSOR_DATA, sensor_data_received)

while True:
    read_messages(bus)

    if datetime.now() - last_request > request_period:
        last_request = datetime.now()

        request_sensor_data(bus)
