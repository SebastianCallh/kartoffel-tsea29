/*
 * i2cslave.c
 *
 * Created: 11/2/2016 3:08:08 PM
 *  Author: antda685
 */ 
#include "common/debug.h"
#include "i2cslave.h"


#include <avr/io.h>
#include <compat/twi.h>
#include <avr/interrupt.h>

void i2c_slave_action(unsigned char read_write_action) {
	//read = 0, write = 1. Derived from buss
	unsigned char test_data = 2;
	unsigned char test_recieve;
	if(read_write_action) {
		DDRD = test_data; //Write data to DDRD
	} else {
		test_recieve = DDRD; //Read data from DDRD
	}
}

#define MAX_DATA_SIZE 255
#define DATA_CMD_LEN 0
#define DATA_CMD_BYTE 1

unsigned char data_size;
unsigned char data_index;
unsigned char data_buffer[MAX_DATA_SIZE];

unsigned char available_data_size;
unsigned char available_data_index;
unsigned char available_data_buffer[MAX_DATA_SIZE];

#define I2C_STATE_UNINIT 0
#define I2C_STATE_WAITING_FOR_ADDR 1
#define I2C_STATE_WAITING_FOR_DATA 2
#define I2C_STATE_READING_DATA 3
unsigned char addr;
unsigned char data;
ISR(TWI_vect) {
	static unsigned char i2c_state = I2C_STATE_UNINIT;
	unsigned char twi_status;
	cli();
	//printf("interrupt happened\n");	
	twi_status = TWSR & 0xF8;
	//printf("%d\n", twi_status);
	switch (twi_status) {		
	case (TW_SR_SLA_ACK) : //SLA+R received, ACK returned
		i2c_state = I2C_STATE_WAITING_FOR_ADDR;
		TWCR |= (1<<TWINT); //Reset TWINT flag
		break;
		
	case (TW_SR_DATA_ACK) : //Data received, ACK returned
		if(i2c_state == I2C_STATE_WAITING_FOR_ADDR) {
			addr = TWDR; //Saving address
			i2c_state = I2C_STATE_WAITING_FOR_DATA;
			//printf("Received address: %d\n", addr);
		} else {
			switch (addr) {
				case DATA_CMD_LEN:
					data_size = TWDR;
					data_index = 0;
					break;
				case DATA_CMD_BYTE:
					data_buffer[data_index] = TWDR;
					++data_index;
					/*
					if (data_index >= data_size) {
						//printf("Received data: ");
						for (int i = 0; i < data_size; ++i) {
							//printf("%c", data_buffer[i]);
						}
						//printf("\n");
					}
					*/
					break;
			}
						
			i2c_state = I2C_STATE_READING_DATA;
			//printf("Received data: %d\n", TWDR);
		}
		TWCR |= (1<<TWINT); //Reset TWINT flag
		break;
		
	case (TW_SR_STOP) : //STOP or START condition received while selected
		if(i2c_state == I2C_STATE_READING_DATA) {
			//Eventually save data somewhere
			//printf("SR_STOP\n");
			i2c_state = I2C_STATE_WAITING_FOR_ADDR;
			
			available_data_size = data_size;
			memcpy(available_data_buffer, data_buffer, data_size);
		}
		TWCR |= (1<<TWINT); //Reset TWINT
		break;
		
	case (TW_ST_DATA_ACK) : //Data transmitted, ACK received
	case (TW_ST_SLA_ACK) : //SLA+R received, ACK returned
		if(i2c_state == I2C_STATE_WAITING_FOR_DATA) {
			switch (addr) {
				case DATA_CMD_LEN:
					available_data_index = 0;
					TWDR = available_data_size;
					break;
				case DATA_CMD_BYTE:
					TWDR = available_data_buffer[available_data_index];
					++available_data_index;
					break;
			}
			
			//printf("Transmitting data: %d \n", data);
			i2c_state = I2C_STATE_WAITING_FOR_ADDR;
		}
		TWCR |= (1<<TWINT); //Reset TWINT
		break;
	case (TW_ST_DATA_NACK) : //Data received, NACK returned
	case (TW_ST_LAST_DATA) : //last data byte transmitted, ACK received
	case (TW_BUS_ERROR) : //Illegal start or stop condition
	default:
		TWCR |= (1 << TWINT); //Reset TWINT
		i2c_state = I2C_STATE_WAITING_FOR_ADDR;
	}
	sei();
}

int main(void)
{
	initialize_uart();
	//printf("Boooooooted\n");
	//Initializing i2cslave
	TWAR = (SLAVE_ADDRESS<<1) & 0xFE; //Sets slavei2caddress and ignore general
	TWDR = 0x00; //Initial data is set to 0
	
	//Starts listening on i2c
	//Reset TW-Interrupt, Enable TW-ACK, TW-Enabled, TW-Interrupt Enable
	TWCR = (1<<TWINT) | (1<<TWEA) | (1<<TWEN) | (1<<TWIE);
	sei();
	for(;;) {
		
	}
	return 1;
}