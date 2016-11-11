/*
 * sensorenhet.c
 *
 * Created: 11/7/2016 11:45:31 AM
 *  Author: antda685
 */ 

#include "common/main.h"
#include "common/protocol.h"
#include <avr/io.h>
#include "common/debug.h"
#include <stdbool.h>

void adc_init(void);
void adc_start(uint8_t channel);
bool adc_ready();
int to_mm(int n);
uint16_t adc_synch(uint8_t channel);
static struct sensor_data sd;
unsigned channel = MUX0;	

void handle_data_request()
{
	return_sensor_data(&sd);
}

void handle_loop()
{
	if (adc_ready()) {
		if (channel == MUX0) {
			sd.ir_right_mm = to_mm(ADCW);
			channel = MUX1;
		}
		else if (channel == MUX1) {
			sd.ir_left_mm = to_mm(ADCW);
			channel = MUX0;
		}
		adc_start(channel);
	}
}

int main(void)
{
	// TODO: Register handlers
	initialize_uart();
	initialize_i2c(0x30);
	adc_init();
	
	printf("BOOT\n");
	
	listen_for_sensor_data_request(&handle_data_request);
	
	return run_program(&handle_loop);
}


void adc_init(void) {
	ADCSRA |= ((1<<ADPS2)|(1<<ADPS1)|(1<<ADPS0));  //FEL MATTE 16Mhz/128 = 125Khz the ADC reference clock
	ADMUX |= ((1<<REFS0)|(1<<REFS1));	//2.56 internal voltage as reference
	//ADMUX |= (1<<REFS0);							//Voltage reference, koppla 3.3v till AREF
	ADCSRA |= (1<<ADEN);							//Turn on ADC
	ADCSRA |= (1<<ADSC);							//Do an initial conversion because this one is the slowest and to ensure that everything is up and running
}

void adc_start(uint8_t channel){
	ADMUX &= 0xE0;             //Clear the older channel that was read
	ADMUX |= channel;          //Defines the new ADC channel to be read
	ADCSRA |= (1<<ADSC);       //Starts a new conversion
}

bool adc_ready(){
	return !(ADCSRA & (1<<ADSC));
}

uint16_t adc_synch(uint8_t channel){
	adc_start(channel);
	while(!adc_ready()) {};            //Wait until the conversion is done
	return ADCW;                    //Returns the ADC value of the chosen channel
}

int to_mm(int n) {
	const int min = 280;
	if (n > min + 720 || min > n) return -1;
	int data[720] = {159, 159, 158, 158, 158, 157, 157, 157, 156, 156, 156, 155, 155, 155, 154, 154, 154, 153, 153, 153, 152, 152, 152, 151, 151, 151, 150, 150, 150, 150, 149, 149, 149, 148, 148, 148, 147, 147, 147, 146, 146, 146, 145, 145, 145, 144, 144, 144, 144, 143, 143, 143, 142, 142, 142, 141, 141, 141, 140, 140, 140, 140, 139, 139, 139, 138, 138, 138, 137, 137, 137, 137, 136, 136, 136, 135, 135, 135, 135, 134, 134, 134, 133, 133, 133, 133, 132, 132, 132, 131, 131, 131, 131, 130, 130, 130, 129, 129, 129, 129, 128, 128, 128, 127, 127, 127, 127, 126, 126, 126, 126, 125, 125, 125, 124, 124, 124, 124, 123, 123, 123, 123, 122, 122, 122, 122, 121, 121, 121, 121, 120, 120, 120, 119, 119, 119, 119, 118, 118, 118, 118, 117, 117, 117, 117, 116, 116, 116, 116, 115, 115, 115, 115, 114, 114, 114, 114, 113, 113, 113, 113, 113, 112, 112, 112, 112, 111, 111, 111, 111, 110, 110, 110, 110, 109, 109, 109, 109, 108, 108, 108, 108, 108, 107, 107, 107, 107, 106, 106, 106, 106, 105, 105, 105, 105, 105, 104, 104, 104, 104, 103, 103, 103, 103, 103, 102, 102, 102, 102, 101, 101, 101, 101, 101, 100, 100, 100, 100, 99, 99, 99, 99, 99, 98, 98, 98, 98, 98, 97, 97, 97, 97, 97, 96, 96, 96, 96, 96, 95, 95, 95, 95, 94, 94, 94, 94, 94, 93, 93, 93, 93, 93, 92, 92, 92, 92, 92, 91, 91, 91, 91, 91, 90, 90, 90, 90, 90, 90, 89, 89, 89, 89, 89, 88, 88, 88, 88, 88, 87, 87, 87, 87, 87, 86, 86, 86, 86, 86, 86, 85, 85, 85, 85, 85, 84, 84, 84, 84, 84, 84, 83, 83, 83, 83, 83, 82, 82, 82, 82, 82, 82, 81, 81, 81, 81, 81, 81, 80, 80, 80, 80, 80, 80, 79, 79, 79, 79, 79, 78, 78, 78, 78, 78, 78, 77, 77, 77, 77, 77, 77, 76, 76, 76, 76, 76, 76, 76, 75, 75, 75, 75, 75, 75, 74, 74, 74, 74, 74, 74, 73, 73, 73, 73, 73, 73, 72, 72, 72, 72, 72, 72, 72, 71, 71, 71, 71, 71, 71, 70, 70, 70, 70, 70, 70, 70, 69, 69, 69, 69, 69, 69, 69, 68, 68, 68, 68, 68, 68, 68, 67, 67, 67, 67, 67, 67, 66, 66, 66, 66, 66, 66, 66, 66, 65, 65, 65, 65, 65, 65, 65, 64, 64, 64, 64, 64, 64, 64, 63, 63, 63, 63, 63, 63, 63, 62, 62, 62, 62, 62, 62, 62, 62, 61, 61, 61, 61, 61, 61, 61, 60, 60, 60, 60, 60, 60, 60, 60, 59, 59, 59, 59, 59, 59, 59, 59, 58, 58, 58, 58, 58, 58, 58, 58, 57, 57, 57, 57, 57, 57, 57, 57, 56, 56, 56, 56, 56, 56, 56, 56, 55, 55, 55, 55, 55, 55, 55, 55, 55, 54, 54, 54, 54, 54, 54, 54, 54, 53, 53, 53, 53, 53, 53, 53, 53, 53, 52, 52, 52, 52, 52, 52, 52, 52, 52, 51, 51, 51, 51, 51, 51, 51, 51, 51, 50, 50, 50, 50, 50, 50, 50, 50, 50, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 47, 47, 47, 47, 47, 47, 47, 47, 47, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 37, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34};
	return data[n - min];
}

/*
intervall 280 < n < 1000
Mätdata från vänster sensor [1023, 872, 761, 664, 590, 531, 476, 430, 400, 374, 350, 327, 304, 289, 271, 258, 239]


//Python för att sampla funktionen
import math
from numpy import arange

min = 280
max = 1000
samples = arange(min, max, 5)
vals = list([int(str(round(29.1 * math.exp(-0.002155 * x), 0)
).replace('.0', '')) for x in range(min, max)])

print(vals)
*/