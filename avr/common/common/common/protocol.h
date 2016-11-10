/*
 * protocol.h
 *
 * Created: 11/7/2016 1:24:20 PM
 *  Author: antda685
 */ 


#ifndef PROTOCOL_H_
#define PROTOCOL_H_


#define CMD_REQUEST_SENSOR_DATA 1
#define CMD_RETURN_SENSOR_DATA 2
#define CMD_PING 3
#define CMD_PONG 4
#define CMD_SET_MOTOR_SPEED 5
#define CMD_SET_LEFT_MOTOR_SPEED 6
#define CMD_SET_RIGHT_MOTOR_SPEED 7

struct sensor_data
{
	int ir_left_mm;
	int ir_right_mm;
};

struct motor_speed
{
	signed char left_speed;
	signed char right_speed;
};

#endif /* PROTOCOL_H_ */