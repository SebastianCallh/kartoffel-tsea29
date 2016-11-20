import RPi.GPIO as GPIO
from time import sleep

#Times in ns
E_CYCLE = 500
E_RISE_FALL = 20
E_PULSE_WIDTH = 230

DATA = [0 for x in range(0, 7)]

'''
Anslutningar till GPIO-portar. Alla portar ar i board-numbering
GPIO 	29, 31, 32, 33, 35, 36, 37, 38
GROUND 	30
5V/VCC 	02
E		40
A		02
K		06
'''

#29 is MSB, 38 LSB
pins = [29, 31, 32, 33, 35, 36, 37, 38]
RS = 22
E = 40

FUNCTION_SET = [0, 0, 1, 1, 0, 0, 0, 0]
DISPLAY_ONOFF_CONTROL = [0, 0, 0, 0, 1, 1, 1, 1] #display, cursor, blink on 
DISPLAY_CLEAR = [0, 0, 0, 0, 0, 0, 0, 1]
ENTRY_MODE_SET = [0, 0, 0, 0, 0, 1, 1, 0] #increment mode, entire shift off
DISPLAY_ON = [0, 0, 0, 0, 1, 1, 0, 0]	


BIT_PATTERN = {
    'A': '01000001',
    'B': '01000010',
    'C': '01000011',
    'D': '01000100',
    'E': '01000101',
    'F': '01000110',
    'G': '01000111',
    'H': '01001000',
    'I': '01001001',
    'J': '01001010',
    'K': '01001011',
    'L': '01001100',
    'M': '01001101',
    'N': '01001110',
    'O': '01001111',
    'P': '01010000',
    'Q': '01010001',
    'R': '01010010',
    'S': '01010011',
    'T': '01010100',
    'U': '01010101',
    'V': '01010110',
    'W': '01010111',
    'X': '01011000',
    'Y': '01011001',
    'Z': '01011010',
    'Å': '11110100',
    'Ö': '11100001',
    '0': '11101111',
    '1': '00110001',
    '2': '00110010',
    '3': '00110011',
    '4': '00110100',
    '5': '00110101',
    '6': '00110110',
    '7': '00110111',
    '8': '00111000',
    '9': '00111001',
    '.': '00101110',
    ' ': '00100000'
}

class LCD:


    def initialize(self):	
        #Use board numbering
        GPIO.setmode(GPIO.BOARD)

        #Configure output pins
        GPIO.setup(RS, GPIO.OUT)
        GPIO.setup(E, GPIO.OUT)
        GPIO.setup(pins, GPIO.OUT)

        sleep_ms(100)				#Make sure at least 30 ms has passed since power on
        
        #Power up sequence
        GPIO.output(RS, 0)		    #Select instruction register
        sleep_us(80)
        self._send(FUNCTION_SET)
        sleep_us(80)				#Make super sure that 39 us has passed
        self._send(DISPLAY_ONOFF_CONTROL)
        sleep_us(80)				#Make super sure that 39 us has passed again
        self._send(DISPLAY_CLEAR)
        sleep_ms(4)				    #Make sure that 1.53 ms has passed
        self._send(ENTRY_MODE_SET)
        sleep_ms(10)
        #End of power up sequence. Display is off

        #Turn on display
        #self._send(DISPLAY_ON)
        sleep_us(80)				#Wait a lot 

    def clear(self):
        self._send(DISPLAY_CLEAR)

    def send(self, data):
        for d in data:
            self._send(self.bit_pattern(d))

    def bit_pattern(self, char):
        return BIT_PATTERN[char.upper()]

    def _send(self, data):
        GPIO.output(E, 0) 		#Make sure E is initially low
        GPIO.output(RS, 1)		#Select data register

        #Put the data on the pins
        for d, p in zip(data, pins):
            GPIO.output(p, int(d))

        #Write the data
        GPIO.output(E, 1)
        sleep_us(1)				#Larger than recommended wait
        GPIO.output(E, 0)
        sleep_us(1)				#Larger than recommended wait


    def cleanup(self):
        GPIO.cleanup()


#Sleep in ms
def sleep_ms(t):
    sleep(t / 1000)


#Sleep in us
def sleep_us(t):
    sleep(t / 10000)
