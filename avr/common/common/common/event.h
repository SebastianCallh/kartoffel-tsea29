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
typedef void(*senor_data_func)(struct sensor_data* sd);
extern void_func sensor_data_request;
extern senor_data_func sensor_data_returned;

void listen_for_sensor_data_request(void_func vf);
void listen_for_sensor_data_returned(senor_data_func sdf);

void notify_sensor_data_request();
void notify_sensor_data_returned(struct sensor_data* sd);



#endif /* EVENT_H_ */