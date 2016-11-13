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
R_W 	22
E		40
A		17
K		06
'''

#29 is MSB, 38 LSB
pins = [29, 31, 32, 33, 35, 36, 37, 38]
RS = 18
R_W = 22
E = 40

FUNCTION_SET = [0, 0, 1, 1, 1, 1, 0, 0]
DISPLAY_ONOFF_CONTROL = [0, 0, 0, 0, 1, 1, 1, 1] #display, cursor, blink on 
DISPLAY_CLEAR = [0, 0, 0, 0, 0, 0, 0, 1]
ENTRY_MODE_SET = [0, 0, 0, 0, 0, 1, 1, 0] #increment mode, entire shift off
DISPLAY_ON = [0, 0, 0, 0, 1, 1, 0, 0]	
	
class LCD:
	def init(self):	
		#Use board numbering
		GPIO.setmode(GPIO.BOARD)
		
		#Configure output pins
		GPIO.setup(RS, GPIO.OUT)
		GPIO.setup(R_W, GPIO.OUT)
		GPIO.setup(E, GPIO.OUT)
		for p in pins:
			GPIO.setup(p, GPIO.OUT)

		GPIO.output(RS, 0)		#Select instruction register
		GPIO.output(E, 0) 		#Make sure E is initially low
		GPIO.output(R_W, 0) 	#Make sure R_W is low (should probably be grounded since we never read)
		
		#Power up sequence
		wait(40)				#Make sure at least 30 ms has passed since power on
		self.send(FUNCTION_SET)
		wait(2)				#Make super sure that 39 us mas passed
		self.send(DISPLAY_ONOFF_CONTROL)
		wait(2)				#Make super sure that 39 us mas passed again
		self.send(DISPLAY_CLEAR)
		wait(4)				#Make sure that 1.53 ms has passed
		self.send(ENTRY_MODE_SET)
		#End of power up sequence. Display is off
		
		#Turn on display
		self.send(DISPLAY_ON)
		sleep()				#Wait a lot 
		
		
			
	def send(self, data):
		GPIO.output(E, 0) 		#Make sure E is initially low
		GPIO.output(RS, 1)		#Select data register
		
		#Put the data on the pins
		for d, p in zip(data, pins):
			GPIO.output(p, d)
			
		#Write the data
		GPIO.output(E, 1)
		wait(1)				#Larger than recommended wait
		GPIO.output(E, 0)
		wait(1)				#Larger than recommended wait
		
		
	def cleanup(self):
		GPIO.cleanup()
		

#Sleep in ms
def wait(t):
	sleep(t / 1000)
		