/*
 * styrenhet.c
 *
 * Created: 11/8/2016 11:32:34 AM
 *  Author: antda685
 */ 

#include "common/main.h"
#include "common/protocol.h"
#include <limits.h>
#include <avr/io.h>
#include "common/debug.h"

const TOP = 16000;
const MAX_SPEED = 16000;

int converted_speed(unsigned char speed) {
	return (speed / 100.0) * MAX_SPEED;
}

void handle_motor_speed_received(struct motor_speed* ms) {
	signed char l = ms->left_speed;
	signed char r = ms->right_speed;
	
	printf("wheel speed received: l: %d, r: %d \n", l, r);
	
	
	if (l < 0) PORTA &= ~(1<<PORTA0);
	if (l >= 0) PORTA |= (1<<PORTA0);
	
	if (r < 0) PORTA &= ~(1<<PORTA2);
	if (r >= 0) PORTA |= (1<<PORTA2);
	
	unsigned char a_l = abs(l) + UINT_MAX + 1;
	unsigned char a_r = abs(r) + UINT_MAX + 1;
	
	printf("abs: l: %d, r: %d \n", a_l, a_r);
	
	int c_l = converted_speed(a_l);
	int c_r = converted_speed(a_r);
	
	printf("converted: l: %d, r: %d \n", c_l, c_r);
	
	OCR1A = c_l;	// Set speed left wheels
	OCR1B = c_r;	// Set speed right wheels
}

void handle_left_motor_speed_received(signed char speed) {
	OCR1A = converted_speed(speed);
}

void handle_right_motor_speed_received(signed char speed) {
	OCR1B = converted_speed(speed);
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
		
	PORTA = 0x05;	// Set direction of wheels (Pin 40 for left wheels, pin 38 for right wheels) (PORTA[0] left and PORTA[2] right)
		
	TCCR1B|= (1<<WGM12)|(1<<CS10)|(1<<WGM13);			// No prescaler, Timer1 settings
	TCCR1A|= (1<<COM1A1)|(1<<WGM11)|(1<<COM1B1);		// Timer1 settings
	ICR1 = TOP;											// Set TOP
	
	// Set initial speed
	OCR1A = 0;
	OCR1B = 0;
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