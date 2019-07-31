#LiChess account
# karel-the-human
# li432qq<3
import os
import time
import random

from browserController import BrowserController
from chessController import ChessController
from utils import Utils
   
print("Starting...")

dragMouseDelay = Utils.loadConfig()

BrowserController.initWeb()
BrowserController.initMouse()



startTime = time.time() #current time in seconds (miliseconds in the decimal values)
startTime = Utils.mySleep(startTime)
while(1==1):        
    #os.system('cls')  # on windows 
    state = BrowserController.readState()
    moveData = ChessController.updateBoardState(state)
    if(moveData != None and (len(moveData)==4 or len(moveData)==5)):
        BrowserController.movePiece(moveData,dragMouseDelay)
    else:
        time.sleep(2)
        BrowserController.aceptarDesafios()
        time.sleep(2)
    
    startTime =  Utils.mySleep(startTime)