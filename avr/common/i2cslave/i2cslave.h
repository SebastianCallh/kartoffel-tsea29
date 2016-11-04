/*
 * i2cslave.h
 *
 * Created: 11/2/2016 3:11:19 PM
 *  Author: antda685
 */ 


#ifndef I2CSLAVE_H_
#define I2CSLAVE_H_
#include "common/queue.h"
#include "common/packet.h"
#define SLAVE_ADDRESS 0x30

void send_data(struct packet*);
struct packet* get_received_data();

#endif /* I2CSLAVE_H_ */