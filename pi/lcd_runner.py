
from lcd import LCD

A = [0, 1, 0, 0, 0, 0, 0, 1]
try:
	lcd = LCD()
	lcd.init()
	lcd.send(A)
		
except e:
	lcd.cleanup()
	print(e)
