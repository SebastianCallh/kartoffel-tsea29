from time import sleep
#from datetime import datetime, timedelta

from accel import Accel
#from driver import Driver

accel = Accel()
accel.initialize()


while (True):
    data = accel.read_data()
    print("x-accel: " + str(data[0]) + " Y-accel: "+ str(data[1]))
    sleep(0.2)
