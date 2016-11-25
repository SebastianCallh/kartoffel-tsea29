"""
This file contains functions for interacting with the two different AVR units.
All functions defined here are outbound which mean they go from the main unit
to one of the AVR units.

The message passing function is implemented as a distributed event bus which
in its distributed nature depends on asynchronous functionality. This means
that messages sent are not executed immediately and there is no guarantee that
the sent command is actually executed on the receiving unit.

For more information see eventbus.py.
"""

from event import Event
from eventbus import EventBus
from protocol import *


# NOTE: Function comments are purposely left out from this file in favor of the
# complete definitions of every found command in proctol.py.

def request_sensor_data():
    EventBus.post(
        SENSOR_ADDR,
        Event(
            message_id=CMD_REQUEST_SENSOR_DATA
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


def bt_return_sensor_data(data):
    EventBus.post(
        BLUETOOTH_ADDR,
        Event(
            message_id=BT_RETURN_SENSOR_DATA,
            arguments=data
        )
    )


def bt_return_servo_data(data):
    EventBus.post(
        BLUETOOTH_ADDR,
        Event(
            message_id=BT_RETURN_SERVO_DATA,
            arguments=data
        )
    )


def bt_return_map_data(data):
    EventBus.post(
        BLUETOOTH_ADDR,
        Event(
            message_id=BT_RETURN_MAP_DATA,
            arguments=data
        )
    )
