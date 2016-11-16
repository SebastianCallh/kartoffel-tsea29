/*
 * outbound.c
 *
 * Created: 11/7/2016 2:13:05 PM
 *  Author: antda685
 */ 
#include "outbound.h"
#include "indexed_packet.h"
#include "i2cslave.h"

void initalize_packet(struct indexed_packet* ip, unsigned char packet_id) {
	struct packet* p = malloc(sizeof(struct packet));	
	ip->p = p;
	ip->index = 0;
	p->size=0;
	write_byte(ip, packet_id);
}

void request_sensor_data() {
	struct indexed_packet ip;
	initalize_packet(&ip, CMD_REQUEST_SENSOR_DATA);
	send_data(ip.p);
}
	
void return_sensor_data(struct sensor_data* sd) {
	struct indexed_packet ip;
	initalize_packet(&ip, CMD_RETURN_SENSOR_DATA);
	write_byte(&ip, sd->ir_left_mm >> 8);
	write_byte(&ip, sd->ir_left_mm & 0xFF);
	write_byte(&ip, sd->ir_right_mm >> 8);
	write_byte(&ip, sd->ir_right_mm & 0xFF);
	send_data(ip.p);
}