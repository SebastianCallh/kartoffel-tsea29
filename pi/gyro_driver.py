from time import sleep
from datetime import datetime, timedelta

from gyro import Gyro
from driver import Driver

gyro = Gyro()
gyro.initialize()

time_delta = datetime.now()
degrees_total = 0

GYRO_LOWER_LIMIT = 10

while(True):
    data = gyro.read_data()

    if abs(data) <= GYRO_LOWER_LIMIT:
        continue
        
    time_delta = time_delta - datetime.now()
    delta_degrees =  data * time_delta.total_seconds()
    degrees_total += delta_degrees
    print(degrees_total)
        