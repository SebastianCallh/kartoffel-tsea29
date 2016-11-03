/*
 * i2cslave.c
 *
 * Created: 11/2/2016 3:08:08 PM
 *  Author: antda685
 */ 

#include "i2cslave.h"


#include <avr/io.h>
#include <compat/twi.h>

void initialize_i2c() {
	TWAR = SLAVE_ADDRESS;
	
}

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

#define I2C_STATE_UNINIT 0
#define I2C_STATE_WAITING_FOR_ADDR 1
#define I2C_STATE_WAITING_FOR_DATA 2
#define I2C_STATE_READING_DATA 3
unsigned char addr;
unsigned char data;
ISR(TWI_vect) {
	
	static unsigned char i2c_state = I2C_STATE_UNINIT;
	unsigned char twi_status;
	
	cli(); //Disables global interrupts
	twi_status = TWSR & 0xF8;
	
	switch (twi_status) {		
	case (TW_SR_SLA_ACK) : //SLA+R received, ACK returned
		i2c_state = I2C_STATE_WAITING_FOR_ADDR;
		TWCR |= (1<<TWINT); //Reset TWINT flag
		break;
		
	case (TW_SR_DATA_ACK) : //Data received, ACK returned
		if(i2c_state == I2C_STATE_WAITING_FOR_ADDR) {
			addr = TWDR; //Saving address
			i2c_state = I2C_STATE_WAITING_FOR_DATA;
		} else {
			data = TWDR; //Saving data
			i2c_state = I2C_STATE_READING_DATA;
		}
		TWCR |= (1<<TWINT); //Reset TWINT flag
		break;
		
	case (TW_SR_STOP) : //STOP or START condition received while selected
		if(i2c_state == I2C_STATE_READING_DATA) {
			//Eventually save data somewhere
			i2c_state = I2C_STATE_WAITING_FOR_ADDR;
		}
		TWCR |= (1<<TWINT); //Reset TWINT
		break;
		
	case (TW_ST_DATA_ACK) : //Data transmitted, ACK received
	case (TW_ST_SLA_ACK) : //SLA+R received, ACK returned
		if(i2c_state == I2C_STATE_WAITING_FOR_DATA) {
			//Eventually set data to what we want to send
			TWDR = data;
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
	
	sei(); //allows global interrupts	
}

int main(void)
{
    while(1)
    {
        //TODO:: Please write your application code 
    }
}