import random
import time

class Utils:

    dragMouseDelay = 1
    minSleep = 3000
    maxSleep = 6000
    
    def loadConfig():
        global minSleep
        global maxSleep
        f= open("config.txt")
        f.readline()
        dragMouseDelay = int(f.readline())
        f.readline()
        minSleep = int(f.readline())        
        f.readline()
        maxSleep = int(f.readline())
        return dragMouseDelay
        
    def mySleep(startTime):
        global minSleep
        global maxSleep
        currentTime = time.time()
        dif = currentTime-startTime
        sleepTime = (random.randint(minSleep, maxSleep)/1000) - dif
        print("Process time: " + str(dif))
        print("Sleep time: " + str(sleepTime))
        if(sleepTime>0):
            time.sleep(sleepTime)
        return time.time()