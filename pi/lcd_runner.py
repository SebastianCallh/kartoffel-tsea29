from time import sleep

from lcd import LCD

A = [0, 1, 0, 0, 0, 0, 0, 1]
ones = [1, 1, 1, 1, 1, 1, 1, 1]
zeroes = [0, 0, 0, 0, 0, 0, 0, 0]

try:
    lcd = LCD()
    lcd.init()
    while True:
        lcd.send(ones)
        sleep(2)
        lcd.send(zeroes)

    lcd.cleanup()
except:
    lcd.cleanup()
