/*
 * common.c
 *
 * Created: 11/1/2016 3:58:23 PM
 *  Author: patsl736
 */ 


#include <avr/io.h>
#include "debug.h"

int main(void)
{
	initialize_uart();
	printf("Device booted.\n");
}