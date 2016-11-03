/*
 * debug.h
 *
 * This header includes a function for initializing the UART functions by enabling the
 * ports RXD0 and TXD0, as well as the internal UART function. The UART interface is
 * made available by substituting stdout.
 *
 * This header also includes stdio.h which exports printf.
 *
 * Created: 11/1/2016 3:59:45 PM
 *  Author: patsl736
 */ 

#include <stdio.h>

#ifndef DEBUG_H_
#define DEBUG_H_

void initialize_uart();

#endif /* DEBUG_H_ */