/*
 * event.c
 *
 * Created: 11/7/2016 1:59:17 PM
 *  Author: antda685
 */ 

#include "event.h";
void_func sensor_data_request;
sensor_data_func sensor_data_returned;

motor_speed_func motor_speed_received;
left_motor_speed_func left_motor_speed_received;
right_motor_speed_func right_motor_speed_received;

//-----------------SENSORENHET-------------------------
void listen_for_sensor_data_request(void_func vf) {
	sensor_data_request = vf;
}

void listen_for_sensor_data_returned(sensor_data_func sdf) {
	sensor_data_returned = sdf;	
}


void notify_sensor_data_request() {
	sensor_data_request();
}

void notify_sensor_data_returned(struct sensor_data* sd) {
	sensor_data_returned(sd);
}


//-----------------STYRENHET-------------------------
void listen_for_motor_speed_received(motor_speed_func msf) {
	motor_speed_received = msf;
}

void listen_for_left_motor_speed_received(left_motor_speed_func lmsf) {
	left_motor_speed_received = lmsf;
}

void listen_for_right_motor_speed_received(right_motor_speed_func rmsf) {
	right_motor_speed_received = rmsf;
}


void notify_motor_speed_received(struct motor_speed* ms) {
	motor_speed_received(ms);
}

void notify_left_motor_speed_received(unsigned char speed) {
	left_motor_speed_received(speed);
}

void notify_right_motor_speed_received(unsigned char speed) {
	right_motor_speed_received(speed);
}
