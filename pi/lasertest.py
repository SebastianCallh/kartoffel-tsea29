from laser import Laser

laser = Laser()

def setup():
    Laser.initialize()

setup()
while(True):
    laser.read_data()
    laser_distance = laser.get_data()
    if laser_distance >0 :
        print("Laser avstånd:"+str(laser_distance)+"\n")
    else:
        print("Error: \n")
