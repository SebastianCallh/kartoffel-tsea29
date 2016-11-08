from bus import STYR_ADDR, SENS_ADDR

CMD_REQUEST_SENSOR_DATA = 1
CMD_RETURN_SENSOR_DATA = 2
CMD_PING = 3
CMD_PONG = 4
CMD_SET_MOTOR_SPEED = 5
CMD_SET_LEFT_MOTOR_SPEED = 6
CMD_SET_RIGHT_MOTOR_SPEED = 7

NUM_CMDS = 7


def request_sensor_data(bus):
    bus.send([CMD_REQUEST_SENSOR_DATA], addr=SENS_ADDR)


def set_motor_speed(bus, left_speed, right_speed=None):
    if right_speed is None:
        right_speed = left_speed

    bus.send([CMD_SET_MOTOR_SPEED, left_speed, right_speed], addr=STYR_ADDR)


def set_left_motor_speed(bus, speed):
    bus.send([CMD_SET_LEFT_MOTOR_SPEED, speed], addr=STYR_ADDR)


def set_right_motor_speed(bus, speed):
    bus.send([CMD_SET_RIGHT_MOTOR_SPEED, speed], addr=STYR_ADDR)
