/*
 * i2cslave.h
 *
 * Created: 11/2/2016 3:11:19 PM
 *  Author: antda685
 */ 


#ifndef I2CSLAVE_H_
#define I2CSLAVE_H_
#include "queue.h"
#include "packet.h"

void send_data(struct packet*);
struct packet* get_received_data();
void initialze_i2c (unsigned char address);

#endif /* I2CSLAVE_H_ */