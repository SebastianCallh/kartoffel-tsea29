import bluetooth
import time

print("In/Out Board")

while True:
    print("Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))

    result = bluetooth.lookup_name('00:15:83:2A:49:E4', timeout=5)
    if (result != None):
        print("John: in")
    else:
        print("John: out")

    result = bluetooth.lookup_name('00:1D:D9:F9:79:43', timeout=5)
    if (result != None):
        print("Paul: in")
    else:
        print("Paul: out")

    time.sleep(60)