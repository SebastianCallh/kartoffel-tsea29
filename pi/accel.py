from time import sleep

import Adafruit_LSM303

lsm303 = Adafruit_LSM303.LSM303()
class Accel:

    @staticmethod
    def read_data():
        try:
            accel, mag = lsm303.read()
            accel_x, accel_y, accel_z = accel
            mag_x, mag_y, mag_z = mag
            return accel_x * 0.001 * 9.82, accel_y * 0.001 * 9.82, accel_z * 0.001 * 9.82,
        except:
            return -1
