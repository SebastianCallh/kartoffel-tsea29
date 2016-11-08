/*
 * styrenhet.c
 *
 * Created: 11/8/2016 11:32:34 AM
 *  Author: antda685
 */ 

#include "common/main.h"
#include "common/protocol.h"
#include <avr/io.h>
#include "common/debug.h"

const TOP = 16000;
const MAX_SPEED = 16000;

int converted_speed(unsigned char speed) {
	return (speed / 100.0) * MAX_SPEED;
}

void handle_motor_speed_received(struct motor_speed* ms) {
	OCR1A = ms->left_speed;	// Set speed left wheels
	OCR1B = ms->right_speed;	// Set speed right wheels
}

void handle_left_motor_speed_received(unsigned char speed) {
	OCR1A = speed;
}

void handle_right_motor_speed_received(unsigned char speed) {
	OCR1B = speed;
}

void handle_loop()
{

}

void initialize_PWM() {
		
	DDRA = 0xFF;	// Set Data Direction on PortA
	DDRD = 0xFF;	// Set Data Direction on PortD
	TCNT1 = 0;		// Reset Timer1 counter
		
	TCCR1A = 0;		// Clear Timer1 settings
	TCCR1B = 0;		// Clear Timer1 settings
		
	PORTA = 0xF5;	// Set direction of wheels (Pin 40 for left wheels, pin 38 for right wheels)
		
	TCCR1B|= (1<<WGM12)|(1<<CS12)|(1<<CS10)|(1<<WGM13); // Prescaler 1024, Timer1 settings
	TCCR1A|= (1<<COM1A1)|(1<<WGM11)|(1<<COM1B1);		// Timer1 settings
	ICR1 = 16;											// Set TOP
		
}

int main(void)
{
	// TODO: Register handlers
	initialize_uart();
	initialize_i2c(0x40);
	initialize_PWM();
	
	listen_for_motor_speed_received(&handle_motor_speed_received);
	listen_for_left_motor_speed_received(&handle_left_motor_speed_received);
	listen_for_right_motor_speed_received(&handle_right_motor_speed_received);
	
	return run_program(&handle_loop);
	
	}

}
