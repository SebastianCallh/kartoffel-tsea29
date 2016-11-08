/*
 * sensorenhet.c
 *
 * Created: 11/7/2016 11:45:31 AM
 *  Author: antda685
 */ 

#include "common/main.h"
#include "common/protocol.h"
#include <avr/io.h>
#include "common/debug.h"

void handle_data_request()
{
	struct sensor_data sd;
	sd.ir_left_mm = 13;
	sd.ir_right_mm = 37;
	
	return_sensor_data(&sd);
}

void handle_data_response(struct sensor_data* sd)
{
	//Not used currently
}

void handle_loop()
{
	
}

int main(void)
{
	// TODO: Register handlers
	initialize_uart();
	initialize_i2c(0x30);
	printf("booted\n");
	listen_for_sensor_data_request(&handle_data_request);
	listen_for_sensor_data_returned(&handle_data_response);
	
	return run_program(&handle_loop);
}
