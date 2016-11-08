/*
 * packet_parser.c
 *
 * Created: 11/7/2016 1:32:55 PM
 *  Author: antda685
 */ 

#include "indexed_packet.h"
#include "protocol.h"

void parse_sensor_data_packet(struct indexed_packet* ip) {
	struct sensor_data* sd = malloc(sizeof(struct sensor_data));
	sd->ir_left_mm = read_byte(ip);
	sd->ir_right_mm = read_byte(ip);
	
	notify_sensor_data_returned(sd);
	free(sd);
}
void parse_and_execute(struct packet* p) {
	struct indexed_packet ip;
	ip.p = p;
	ip.index = 0;
	unsigned char cmd_id = read_byte(&ip);
	
	switch (cmd_id) {
		case (CMD_REQUEST_SENSOR_DATA):
			notify_sensor_data_request();
			break;
		case (CMD_RETURN_SENSOR_DATA):
			parse_sensor_data_packet(&ip);
			break;
		case (CMD_PING):
			break;
		case (CMD_PONG):
			break;
		default:
			break;
	}
	
	free(p);
}
