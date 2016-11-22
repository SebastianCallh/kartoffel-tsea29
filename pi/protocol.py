"""
The protocol for the robot consist of various commands, or events, passed along
the main bus using a distributed event bus. Each command is identified by its
command id and is transmitted before eventual arguments.

All commands may be sent in any direction but the implementations will probably
choose to ignore irrelevant one. For messages originating from the main unit,
see outbound.py.
"""

# Addresses for the units on the bus. Note that the laser cannot be queried
# using the protocol described in bus.py.

SENSOR_ADDR = 0x30
STYR_ADDR = 0x40
LASER_ADDR = 0x62

# Packet addresses
PACKET_HEADER = 0
PACKET_DATA = 1


# Request data from the sensor unit
CMD_REQUEST_SENSOR_DATA = 1
"""
Issues a request to the sensor unit prompting it to send its most recent sensor
data back to the main unit. As the data transfer is asynchronous the sensor
unit responds to the request by posting a CMD_RETURN_SENSOR_DATA command on the
bus.

Target: Sensor unit

Arguments: None
"""


# Return sensor data from the sensor unit
CMD_RETURN_SENSOR_DATA = 2
"""
Command sent from the sensor unit after a request for its sensor data has been
made. As data from various sensors are reported independently it is not certain
that the value from sensor A and value from sensor B reflect the world at the
same point in time.

Target: Main unit

Arguments:
ir_left_mm (2 bytes, two's complement)
    Distance recorded by the left IR sensor in mm, or -1 if the distance is not
    within the supported range.
ir_right_mm (2 bytes, two's complement)
    Distance recorded by the right IR sensor in mm, or -1 if the distance is
    not within the supported range.
"""


# Ping a unit
CMD_PING = 3
"""
Dummy command which will only trigger the other unit to respond with a PONG
command. Preferably used to test a connection without forcing the other party
to perform any actual action.

Target: Any AVR unit

Arguments: None
"""


# Pong a unit
CMD_PONG = 4
"""
Reply to a PING command.

Target: Main unit

Arguments: None
"""


# Set both motor speeds in the control unit
CMD_SET_MOTOR_SPEED = 5
"""
Sets the speed of both the left and right motors on the robot. Values can
be both positive and negative and the range -100 to 100 is supported, where the
value represents a percentage of the max speed. It seems like the different
directions have various max speeds, which has to be considered when
implementing on-spot-rotation or other actions which assume equal speed forward
and backwards.

Target: Control unit

Arguments:
left_motor_speed (1 byte, positive or negative)
    Left motor speed in percentage of max speed ranging from -100 to 100.
right_motor_speed (1 byte, positive or negative)
    Right motor speed in percentage of max speed ranging from from -100 to 100.
"""


# Set left motor speed only in control unit
CMD_SET_LEFT_MOTOR_SPEED = 6
"""
Sets the speed of the left motors on the robot. It is only possible to pass
positive values with the command in the range 0 to 100, where the value
represent a percentage of the max speed.

Target: Control unit

Arguments:
speed (1 byte, positive)
    Left motor speed in percentage of max speed ranging from 0 to 100.
"""


# Set right motor speed in the control unit
CMD_SET_RIGHT_MOTOR_SPEED = 7
"""
Sets the speed of the right motors on the robot. It is only possible to pass
positive values with the command in the range 0 to 100, where the value
represent a percentage of the max speed.

Target: Control unit

Arguments:
speed (1 byte, positive)
    Right motor speed in percentage of max speed ranging from 0 to 100.
"""


# Indicates that the robot has started turning
"""
Event called internally within the main unit to indicate that a simple 90
degree turn has been initiated.

Target: Main unit

Arguments: None
"""
CMD_TURN_STARTED = 8


# Indicates that the robot has stopped turning
"""
Event called internally within the main unit to indicate that a simple 90
degree turn has finished.

Target: Main unit

Arguments:
is_right_turn (1 byte, boolean)
    True for right turn, false for left turn.
"""
CMD_TURN_FINISHED = 9
