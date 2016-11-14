
from lcd import LCD

A = [0, 1, 0, 0, 0, 0, 0, 1]
try:
	lcd = LCD()
	lcd.init()
	lcd.send(A)
	lcd.cleanup()
	
except e:
	lcd.cleanup()
	print(e)
