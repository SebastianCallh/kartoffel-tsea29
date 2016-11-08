/*
 * event.h
 *
 * Created: 11/7/2016 1:53:46 PM
 *  Author: antda685
 */ 


#ifndef EVENT_H_
#define EVENT_H_
#include "protocol.h"
typedef void(*void_func)();
typedef void(*sensor_data_func)(struct sensor_data* sd);

typedef void(*motor_speed_func)(struct motor_speed* ms);
typedef void(*left_motor_speed_func)(unsigned char speed);
typedef void(*right_motor_speed_func)(unsigned char speed);

extern void_func sensor_data_request;
extern sensor_data_func sensor_data_returned;

extern motor_speed_func motor_speed_received;
extern left_motor_speed_func left_motor_speed_received;
extern right_motor_speed_func right_motor_speed_received;

//-----------------SENSORENHET-------------------------
void listen_for_sensor_data_request(void_func vf);
void listen_for_sensor_data_returned(sensor_data_func sdf);

void notify_sensor_data_request();
void notify_sensor_data_returned(struct sensor_data* sd);

//-----------------STYRENHET-------------------------
void listen_for_motor_speed_received(motor_speed_func msf);
void listen_for_left_motor_speed_received(left_motor_speed_func lmsf);
void listen_for_right_motor_speed_received(right_motor_speed_func rmsf);

void notify_motor_speed_received(struct motor_speed* ms);
void notify_left_motor_speed_received(unsigned char speed);
void notify_right_motor_speed_received(unsigned char speed);



#endif /* EVENT_H_ */