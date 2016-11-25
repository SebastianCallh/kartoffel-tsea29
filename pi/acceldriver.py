from time import sleep
#from datetime import datetime, timedelta

from accel import Accel
#from driver import Driver

accel = Accel()

while (True):
    data = accel.read_data()
    print("x-accel: " + str(data))
    sleep(0.2)
