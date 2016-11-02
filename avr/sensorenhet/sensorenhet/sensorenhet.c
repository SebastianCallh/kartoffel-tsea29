/*
 * sensorenhet.c
 *
 * Created: 11/2/2016 8:27:57 AM
 *  Author: matsj696
 */ 


#include <avr/io.h>
#include "debug.h";

int main(void)
{
	initialize_uart();
	
	// Output
	DDRA = 0xFF;
	
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));    //Prescaler at 128 (when used with 16MHz clock, we get 125Khz)
	
	//ADC0 input
	ADMUX = 0x40;
	
	ADCSRB &= ~((1<<ADTS2)|(1<<ADTS1)|(1<<ADTS0));    //ADC in free-running mode
	ADCSRA |= (1<<ADATE);                //Signal source, in this case is the free-running
	ADCSRA |= (1<<ADEN);                //Power up the ADC
	ADCSRA |= (1<<ADSC);                //Start converting
    
	int adc_value;
	while(1)
    {
		adc_value = ADCW;  
		printf("Value: %d\n", adc_value);
	}
}