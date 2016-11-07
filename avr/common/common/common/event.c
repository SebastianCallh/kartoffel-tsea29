/*
 * event.c
 *
 * Created: 11/7/2016 1:59:17 PM
 *  Author: antda685
 */ 

#include "event.h";
void_func sensor_data_request;
senor_data_func sensor_data_returned;

void listen_for_sensor_data_request(void_func vf) {
	sensor_data_request = vf;
}

void listen_for_sensor_data_returned(senor_data_func sdf) {
	sensor_data_returned = sdf;	
}

void notify_sensor_data_request() {
	sensor_data_request();
}

void notify_sensor_data_returned(struct sensor_data* sd) {
	sensor_data_returned(sd);
}