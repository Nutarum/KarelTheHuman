import random
import time

class Utils:

    def mySleep(startTime):
        currentTime = time.time()
        dif = currentTime-startTime
        sleepTime = (random.randint(3000, 6000)/1000) - dif
        print("Process time: " + str(dif))
        print("Sleep time: " + str(sleepTime))
        if(sleepTime>0):
            time.sleep(sleepTime)
        return time.time()