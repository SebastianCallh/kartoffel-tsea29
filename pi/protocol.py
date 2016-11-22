"""
The protocol for the robot consist of various commands, or events, passed along
the main bus using a distributed event bus. Each command is identified by its
command id and is transmitted before eventual arguments.

All commands may be sent in any direction but the implementations will probably
choose to ignore irrelevant one. For messages originating from the main unit,
see outbound.py.
"""
BLUETOOTH_ADDR = 0xBEEF



# Request data from the sensor unit
CMD_REQUEST_SENSOR_DATA = 1
"""
Issues a request to the sensor unit prompting it to send its most recent sensor
data back to the main unit. As the data transfer is asynchronous the sensor unit
responds to the request by posting a CMD_RETURN_SENSOR_DATA command on the bus.

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
    Distance recorded by the right IR sensor in mm, or -1 if the distance is not
    within the supported range.
"""


# Ping a unit
CMD_PING = 3
"""
Dummy command which will only trigger the other unit to respond with a PONG
command. Preferably used to test a connection without forcing the other party to
perform any actual action.

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
directions have various max speeds, which has to be considered when implementing
on-spot-rotation or other actions which assume equal speed forward and
backwards.

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

#-------------------- Bluetooth commands ---------------------



REQUEST_PI_IP = 10
RETURN_PI_IP = 11

TEST_HI = 12
TEST_HO = 13

BT_SERVER_RESTART = 14

BT_SERVER_EXIT = 15

BT_REQUEST_SENSOR_DATA = 16

BT_REQUEST_MAP_DATA = 17

BT_REQUEST_SERVO_DATA = 18

BT_SEND_SENSOR_DATA = 19

BT_SEND_MAP_DATA = 20

BT_SEND_SERVO_DATA = 21


#TODO: If queue works properly, these lists won't be necessary
# List of commands that are of the type data requests, i.e. the client requests
# data from server
DATA_REQUESTS = [REQUEST_PI_IP, TEST_HI]

# List of commands that are of the type direct operations, which 
# controls the robot (or bluetooth server) directly.  
# The client does not excpect an answer.
DIRECT_OPERATIONS = [BT_SERVER_RESTART, BT_SERVER_EXIT]











