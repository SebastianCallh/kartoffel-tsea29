from gyro import Gyro
from time import sleep

gyro = Gyro()
gyro.initialize()


while(True):
    sleep(0.2)
    data = gyro.read_data()
    print(data)