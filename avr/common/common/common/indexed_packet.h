/*
 * packet_reader.h
 *
 * Created: 11/7/2016 1:18:42 PM
 *  Author: antda685
 */ 


#ifndef PACKET_READER_H_
#define PACKET_READER_H_

#include "packet.h"

struct indexed_packet
{
	unsigned int index;
	struct packet* p;
};

unsigned char read_byte(struct indexed_packet* p);
void write_byte(struct indexed_packet* p, unsigned char byte);

#endif /* PACKET_READER_H_ */