/*
 * sensorenhet.c
 *
 * Created: 11/2/2016 8:27:57 AM
 *  Author: matsj696
 */ 


#include <avr/io.h>
#include <stdbool.h>
#include "debug.h"

int channel;
bool adc_has_data;
uint16_t adc_data;					//Variable used to store the value read from the ADC
void adc_init(void);				//Function to initialize/configure the ADC
uint16_t adc_read(uint8_t channel);	//Function to read an arbitrary analogic channel/pin

void adc_init(void) {
	 ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));  //FEL MATTE 16Mhz/128 = 125Khz the ADC reference clock
	 ADMUX |= (1<<REFS0);							//Voltage reference, koppla 3.3v till AREF
	 ADCSRA |= (1<<ADEN);							//Turn on ADC
	 ADCSRA |= (1<<ADSC);							//Do an initial conversion because this one is the slowest and to ensure that everything is up and running
 }
 
 //BUSY WAITAR. JÄTTEDÅLIGT.
 uint16_t adc_read(uint8_t channel){
	 ADMUX &= 0xF0;             //Clear the older channel that was read
	 ADMUX |= channel;          //Defines the new ADC channel to be read
	 ADCSRA |= (1<<ADSC);       //Starts a new conversion
	 while(ADCSRA & (1<<ADSC)); //Wait until the conversion is done
	 return ADCW;			    //Returns the ADC value of the chosen channel
 }
 
 void adc_start(uint8_t channel){
	 ADMUX &= 0xF0;             //Clear the older channel that was read
	 ADMUX |= channel;          //Defines the new ADC channel to be read
	 ADCSRA |= (1<<ADSC);       //Starts a new conversion
}
 
 bool adc_ready(){
	return !(ADCSRA & (1<<ADSC));
}

int main(void)
{
	initialize_uart();
	adc_init();
	
	channel = MUX0;
	while(1)
    {
		if (adc_ready()) {
			adc_data = ADCW;
			printf("latest data from channel %d: %d, \n", channel, adc_data);
		}
		
		if (adc_ready()){
			adc_start(channel);
			if (channel == MUX0) {
				channel = MUX1;
				} else if (channel == MUX1) {
				channel = MUX0;
			}
		}
	}
}