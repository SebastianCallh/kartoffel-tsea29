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

from eventbus import EventBus
from protocol import *
from bt_task import BT_task


# NOTE: Function comments are purposely left out from this file in favor of the
# complete definitions of every found command in proctol.py.

def request_ip():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            REQUEST_PI_IP
        )
    )


def bt_request_sensor_data():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_REQUEST_SENSOR_DATA
        )
    )


def bt_request_servo_data():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_REQUEST_SERVO_DATA
        )
    )


def bt_request_map_data():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_REQUEST_MAP_DATA
        )
    )


def bt_drive_forward():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_DRIVE_FORWARD
        )
    )


def bt_drive_back():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_DRIVE_BACK
        )
    )


def bt_turn_right():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_TURN_RIGHT
        )
    )

def bt_forward_right():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_DRIVE_FORWARD_RIGHT
        )
    )

def bt_turn_left():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_TURN_LEFT
        )
    )

def bt_forward_left():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_DRIVE_FORWARD_LEFT
        )
    )

def bt_shutdown():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_SERVER_SHUTDOWN
        )
    )


def bt_restart():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            BT_SERVER_RESTART
        )
    )

def bt_switch_to_auto():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            AUTONOMOUS_MODE
        )
    )


def bt_switch_to_manual():
    EventBus.post(
        BLUETOOTH_ADDR,
        BT_task(
            MANUAL_MODE
        )
    )
