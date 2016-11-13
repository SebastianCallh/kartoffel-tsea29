import RPi.GPIO as GPIO


#Times in ns
E_CYCLE = 500
E_RISE_FALL = 20
E_PULSE_WIDTH = 230
DATA = [0 for x in range(0, 7)]

'''
Anslutningar till GPIO-portar
GPIO 	29, 31, 32, 33, 35, 36, 37, 38
GROUND 	30
5V/VCC 	02
R_W 	22
E		40
'''

pins = [29, 31, 32, 33, 35, 36, 37, 38]
R_W = 22
E = 40

class LCD:
	def init(self):	
		#Use board numbering
		GPIO.setmode(GPIO.BOARD)
		
		GPIO.setup(R_W, GPIO.OUT)
		GPIO.setup(E, GPIO.OUT)
		print('R_W, E output')
		
		for p in pins:
			GPIO.setup(p, GPIO.OUT)
			print('pin ' + p ' + 'output')
			
			
	def send(self, data):
		for d, p in zip(data, pins):
			GPIO.output(p, d)
			print('setting ' + p + ' to ' + d)
			
	def cleanup(self):
		GPIO.cleanup()