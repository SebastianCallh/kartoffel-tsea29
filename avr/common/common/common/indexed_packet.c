/*
 * packet_reader.c
 *
 * Created: 11/7/2016 1:20:59 PM
 *  Author: antda685
 */ 
#include "indexed_packet.h"


unsigned char read_byte(struct indexed_packet* p) {
	
	unsigned char byte = p->p->data[p->index];
	++p->index;
	return byte;
}

void write_byte(struct indexed_packet* p, unsigned char byte) {
	p->p->data[p->index] = byte;
	++p->index;
	++p->p->size;
}