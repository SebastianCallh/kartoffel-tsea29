/*
 * common.c
 *
 * Created: 11/1/2016 3:58:23 PM
 *  Author: patsl736
 */ 


#include <avr/io.h>
#include "debug.h"

void initialize_PWM();
void set_robot_speed(int speed);

int main(void)
{
	
	initialize_uart();
	initialize_PWM();
	set_robot_speed(2);
		
	int counter = 0;
	while (1) {

		
		counter = TCNT1;
		if(counter < 0) {
			printf("counter negative");
		}
		else{
			printf("Counter value: %d\n", TCNT1);
		}
	}
}

void set_robot_speed(int speed) {
	OCR1A = speed;	// Set speed left wheels
	OCR1B = speed;	// Set speed right wheels
			
}

void initialize_PWM() {
	
	DDRA = 0xFF;	// Set Data Direction on PortA
	DDRD = 0xFF;	// Set Data Direction on PortD
	TCNT1 = 0;		// Reset Timer1 counter
	
	TCCR1A = 0;		// Clear Timer1 settings
	TCCR1B = 0;		// Clear Timer1 settings
		
	PORTA = 0xF1;	// Set direction of wheels (Pin 40 for left wheels, pin 38 for right wheels)
		
	TCCR1B|= (1<<WGM12)|(1<<CS12)|(1<<CS10)|(1<<WGM13); // Prescaler 1024, Timer1 settings
	TCCR1A|= (1<<COM1A1)|(1<<WGM11)|(1<<COM1B1);		// Timer1 settings
	ICR1 = 16;											// Set TOP	
	
}

