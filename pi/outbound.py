"""
This file contains functions for interacting with the two different AVR units.
All functions defined here are outbound which mean they go from the main unit
to one of the AVR units.

The message passing function is implemented as a distributed event bus which
in its distributed nature depends on asynchronous functionality. This means that
messages sent are not executed immediately and there is no guarantee that the
sent command is actually executed on the receiving unit.

For more information see eventbus.py.
"""

from bus import STYR_ADDR, SENSOR_ADDR
from event import Event
from eventbus import EventBus
from protocol import CMD_REQUEST_SENSOR_DATA, CMD_SET_MOTOR_SPEED, \
    CMD_SET_LEFT_MOTOR_SPEED, CMD_SET_RIGHT_MOTOR_SPEED, \
    BT_REQUEST_MAP_DATA, BT_REQUEST_SENSOR_DATA, BT_REQUEST_SERVO_DATA, \
    BT_SEND_MAP_DATA, BT_SEND_SENSOR_DATA, BT_SEND_SERVO_DATA, RETURN_PI_IP, TEST_HO, BLUETOOTH_ADDR

# NOTE: Function comments are purposely left out from this file in favor of the
# complete definitions of every found command in proctol.py.


def return_ip(ip):
    EventBus.post(
        BLUETOOTH_ADDR,
        Event(
            message_id=RETURN_PI_IP,
            arguments=[
                ip
            ]
        )
    )

def test_ho():
    EventBus.post(
        BLUETOOTH_ADDR,
        Event(
            message_id=TEST_HO,
            arguments=[
                "ho"
            ]
        )
    )


def request_sensor_data():
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=CMD_REQUEST_SENSOR_DATA
        )
    )


def bt_request_sensor_data():
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=BT_REQUEST_SENSOR_DATA
        )
    )


def bt_request_map_data():
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=BT_REQUEST_MAP_DATA
        )
    )


def bt_request_servo_data():
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=BT_REQUEST_SERVO_DATA
        )
    )


def bt_send_sensor_data(data):
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=BT_SEND_SENSOR_DATA,
            arguments=data
        )
    )


def bt_send_map_data(data):
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=BT_SEND_MAP_DATA,
            arguments=data
        )
    )


def bt_send_servo_data(data):
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=BT_SEND_SERVO_DATA,
            arguments=data
        )
    )



def set_motor_speed(left_speed, right_speed=None):
    if right_speed is None:
        right_speed = left_speed

    EventBus.post(
        STYR_ADDR,
        Event(
            message_id=CMD_SET_MOTOR_SPEED,
            arguments=[
                left_speed,
                right_speed
            ]
        )
    )


def set_left_motor_speed(speed):
    EventBus.post(
        STYR_ADDR,
        Event(
            message_id=CMD_SET_LEFT_MOTOR_SPEED,
            arguments=[
                speed
            ]
        )
    )


def set_right_motor_speed(speed):
    EventBus.post(
        STYR_ADDR,
        Event(
            message_id=CMD_SET_RIGHT_MOTOR_SPEED,
            arguments=[
                speed
            ]
        )
    )
