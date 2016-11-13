
from lcd import LCD

try:
	lcd = LCD()
	lcd.init()
	lcd.send([1, 1, 1, 1, 1, 1, 1, 1])
		
except e:
	lcd.cleanup()
	print(e)
