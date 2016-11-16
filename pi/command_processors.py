"""
Contains various pre-notify command processors used to parse received data into
more usable form than single bytes.
"""
from protocol import CMD_RETURN_SENSOR_DATA
from utils import twos_comp

COMMAND_PROCESSORS = {}


def process_arguments(message_id, arguments):
    if message_id in COMMAND_PROCESSORS:
        return COMMAND_PROCESSORS[message_id](*arguments)

    return arguments


# Sensor data contains some arguments stored in 16-bit two's complement which
# must be parsed into it's corresponding python values.
def process_sensor_data(left_ir_mm_hi, left_ir_mm_lo, right_ir_mm_hi, right_ir_mm_lo, *args):
    left_ir_mm = twos_comp((left_ir_mm_hi << 8) | left_ir_mm_lo, 16)
    right_ir_mm = twos_comp((right_ir_mm_hi << 8) | right_ir_mm_lo, 16)

    return [left_ir_mm, right_ir_mm] + list(args)


COMMAND_PROCESSORS[CMD_RETURN_SENSOR_DATA] = process_sensor_data
