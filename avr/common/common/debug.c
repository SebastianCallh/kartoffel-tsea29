/*
 * debug.c
 *
 * Created: 11/1/2016 3:59:37 PM
 *  Author: patsl736
 */ 

#include "config.h"
#include "debug.h"

#include <avr/io.h>
#include <inttypes.h>
#include <assert.h>

#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

void USARTWriteChar(char data);
int USARTPutChar(char data, FILE *stream);

static FILE uart_stdout = FDEV_SETUP_STREAM(USARTPutChar, NULL, _FDEV_SETUP_WRITE);

bool uart_initialized = false;

void initialize_uart() {
	// Set baud rate
	UBRR0L = BAUD_PRESCALE;
	UBRR0H = (BAUD_PRESCALE>>8);
	
	// Enable RX and TX for USART
	UCSR0B=(1<<RXEN0)|(1<<TXEN0);
	
	// Redirect stdout to UART
	stdout = &uart_stdout;
	
	// Keep track of state to detect errors early
	uart_initialized = true;
}

void USARTWriteChar(char data)
{
	while(!(UCSR0A & (1<<UDRE0)))
	{
		// Busy wait until we can send data
	}

	UDR0=data;
}


int USARTPutChar(char data, FILE *stream)
{
	// Fail hard if UART is not initialized
	assert(uart_initialized);
	
	// Include carriage return to start at beginning of line
	if (data == '\n')
	{
		USARTWriteChar('\r');
	}
	
	USARTWriteChar(data);
	return 0;
}
