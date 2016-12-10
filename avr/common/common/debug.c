/*
 * debug.c
 *
 * Created: 11/1/2016 3:59:37 PM
 *  Author: patsl736
 */ 

#include "config.h"
#include "debug.h"

#include <avr/io.h>
#include <avr/interrupt.h>
#include <inttypes.h>
#include <assert.h>
#include <stdbool.h>

#define BAUD_PRESCALE (((F_CPU / (USART_BAUDRATE * 16UL))) - 1)

int USARTPutChar(char data, FILE *stream);

static FILE uart_stdout = FDEV_SETUP_STREAM(USARTPutChar, NULL, _FDEV_SETUP_WRITE);

bool uart_initialized = false;
char data_to_write[1024];
unsigned char write_data_index = 0;
unsigned char read_data_index = 0;
unsigned int data_available = 0;

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
	data_to_write[write_data_index] = data;
	++write_data_index;
	++data_available;		
	UCSR0B |= (1<<UDRIE0);
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

ISR(USART0_UDRE_vect) {	
	if (data_available > 0) {
		char data = data_to_write[read_data_index];
		++read_data_index;
		--data_available;

		UDR0=data;
		if (data_available == 0) {
			read_data_index = 0;
			write_data_index = 0;
			UCSR0B &= ~(1<<UDRIE0);
		}
	} else {
		USARTWriteChar('-');
	}
}
