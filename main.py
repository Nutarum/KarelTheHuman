#LiChess account
# karel-the-human
# li432qq<3
import os
import time
import random

from browserController import BrowserController
from chessControler import ChessControler
from utils import Utils
   
print("Starting...")

BrowserController.initWeb()
BrowserController.initMouse()

startTime = time.time() #current time in seconds (miliseconds in the decimal values)
startTime = Utils.mySleep(startTime)
while(1==1):    
    os.system('cls')  # on windows          
    moveData = ChessControler.updateBoardState(BrowserController.readState())
    if(len(moveData)==4):
        BrowserController.movePiece(moveData)
    startTime =  Utils.mySleep(startTime)