from time import sleep
from datetime import datetime, timedelta

from gyro import Gyro
from driver import Driver

gyro = Gyro()
gyro.initialize()

previous_time = datetime.now()
degrees_total = 0

GYRO_LOWER_LIMIT = 10

while(True):
    data = gyro.read_data()
    
    time_delta = (previous_time - datetime.now()).total_seconds()
    delta_degrees =  data * time_delta
    previous_time = datetime.now()

    #Has to be run after previous time is set
    if abs(data) <= GYRO_LOWER_LIMIT:
        continue
    
    degrees_total += delta_degrees
    print(degrees_total)
        