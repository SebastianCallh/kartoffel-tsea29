from datetime import datetime, timedelta

from bus import Bus
from messages import read_messages, subscribe_to_cmd
from outbound import request_sensor_data, CMD_RETURN_SENSOR_DATA

bus = Bus()

last_request = datetime.now()
request_period = timedelta(milliseconds=1)
busy = False


def sensor_data_received(msg):
    global busy
    busy = False

    ir_left_mm = msg[1]
    ir_right_mm = msg[2]

    print('ir_left_mm: ' + str(ir_left_mm))
    print('ir_right_mm: ' + str(ir_right_mm))


subscribe_to_cmd(CMD_RETURN_SENSOR_DATA, sensor_data_received)

while True:
    read_messages(bus)

    if not busy and datetime.now() - last_request > request_period:
        busy = True
        last_request = datetime.now()

        request_sensor_data(bus)
