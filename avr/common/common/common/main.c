/*
 * main.c
 *
 * Created: 11/7/2016 11:43:49 AM
 *  Author: antda685
 */ 

#include "main.h"
#include "packet.h"
int run_program(loopHandler handler)
{
	// TODO: Init
	
	for (;;)
	{
		struct packet* p;
		while (p = get_received_data()) {
			parse_and_execute(p);
		}
		
		handler();
	}
}
