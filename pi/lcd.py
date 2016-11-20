import RPi.GPIO as GPIO
from time import sleep

'''
Anslutningar till GPIO-portar. Alla portar ar i board-numbering
GPIO 	29, 31, 32, 33, 35, 36, 37, 38
GROUND 	30
5V/VCC 	02
E		40
A		02
K		06
'''


#Times in ns
E_CYCLE = 500
E_RISE_FALL = 20
E_PULSE_WIDTH = 230

DATA = [0 for x in range(0, 7)]


#29 is MSB, 38 LSB
PINS = [29, 31, 32, 33, 35, 36, 37, 38]
RS = 22
E = 40

FUNCTION_SET = [0, 0, 1, 1, 0, 0, 0, 0]
DISPLAY_ONOFF_CONTROL = [0, 0, 0, 0, 1, 0, 1, 1] #display, cursor, blink on 
DISPLAY_CLEAR = [0, 0, 0, 0, 0, 0, 0, 1]
ENTRY_MODE_SET = [0, 0, 0, 0, 0, 1, 1, 0] #increment mode, entire shift off
DISPLAY_ON = [0, 0, 0, 0, 1, 1, 1, 1]	
RESET_CURSOR = [0, 0, 0, 0, 0, 0, 1]

BIT_PATTERN = {
    'A': [0,1,0,0,0,0,0,1},
    'B': [0,1,0,0,0,0,1,0],
    'C': [0,1,0,0,0,0,1,1],
    'D': [0,1,0,0,0,1,0,0],
    'E': [0,1,0,0,0,1,0,1],
    'F': [0,1,0,0,0,1,1,0],
    'G': [0,1,0,0,0,1,1,1],
    'H': [0,1,0,0,1,0,0,0],
    'I': [0,1,0,0,1,0,0,1],
    'J': [0,1,0,0,1,0,1,0],
    'K': [0,1,0,0,1,0,1,1],
    'L': [0,1,0,0,1,1,0,0],
    'M': [0,1,0,0,1,1,0,1],
    'N': [0,1,0,0,1,1,1,0],
    'O': [0,1,0,0,1,1,1,1],
    'P': [0,1,0,1,0,0,0,0],
    'Q': [0,1,0,1,0,0,0,1],
    'R': [0,1,0,1,0,0,1,0],
    'S': [0,1,0,1,0,0,1,1],
    'T': [0,1,0,1,0,1,0,0],
    'U': [0,1,0,1,0,1,0,1],
    'V': [0,1,0,1,0,1,1,0],
    'W': [0,1,0,1,0,1,1,1],
    'X': [0,1,0,1,1,0,0,0],
    'Y': [0,1,0,1,1,0,0,1],
    'Z': [0,1,0,1,1,0,1,0],
    '0': [1,1,1,0,1,1,1,1],
    '1': [0,0,1,1,0,0,0,1],
    '2': [0,0,1,1,0,0,1,0],
    '3': [0,0,1,1,0,0,1,1],
    '4': [0,0,1,1,0,1,0,0],
    '5': [0,0,1,1,0,1,0,1],
    '6': [0,0,1,1,0,1,1,0],
    '7': [0,0,1,1,0,1,1,1],
    '8': [0,0,1,1,1,0,0,0],
    '9': [0,0,1,1,1,0,0,1],
    '.': [0,0,1,0,1,1,1,0],
    ' ': [0,0,1,0,0,0,0,0]
}

class LCD:


    def initialize(self):	
        #Use board numbering
        GPIO.setmode(GPIO.BOARD)

        #Configure output pins
        GPIO.setup(RS, GPIO.OUT)
        GPIO.setup(E, GPIO.OUT)
        GPIO.setup(PINS, GPIO.OUT)


        #Power up sequence
        GPIO.output(RS, 0)		    #Select instruction register
        sleep_ms(100)				#Make sure at least 30 ms has passed since power on
        
        
        self._send(FUNCTION_SET)
        sleep_ms(10)
        
        self._send(FUNCTION_SET)
        sleep_us(200)
        
        self._send(FUNCTION_SET)
        sleep_ms(200)
        
        
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
        self._send(DISPLAY_ON)


    def clear(self):
        GPIO.output(RS, 0)
        self._send(DISPLAY_CLEAR)


    def reset_cursor(self):
        GPIO.output(RS, 0)
        self._send(RESET_CURSOR)


    def send(self, data):
        self.clear()
        self.reset_cursor()
        
        GPIO.output(RS, 1)		#Select data register
        
        for d in data:
            self._send(self.bit_pattern(d))

   
    def bit_pattern(self, char):
        return BIT_PATTERN[char.upper()]


    def _send(self, data):
        GPIO.output(E, 0) 		#Make sure E is initially low

        #Put the data on the pins
        for d, p in zip(data, PINS):
            GPIO.output(p, d)

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
