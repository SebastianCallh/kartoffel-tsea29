/*
 * outbound.h
 *
 * Created: 11/7/2016 2:11:52 PM
 *  Author: antda685
 */ 


#ifndef OUTBOUND_H_
#define OUTBOUND_H_

#include "protocol.h"

void request_sensor_data();
void return_sensor_data(struct sensor_data* sd);


#endif /* OUTBOUND_H_ */