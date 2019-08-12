import numpy as np
import random
import chess
from karelthetrainer.karelthehumanV2 import KarelTheHumanV2 as KarelTheHuman

board = chess.Board()
bot = KarelTheHuman()
print("Versión del bot cargada: " + str(bot))

class ChessController: 
    def clearBoard():        
        global board        
        board = chess.Board()
    
    #receive the board orientation, the player to move, and the list of moves (in algebraic notation)
    def updateBoardState(data):
        global board      
        global bot
        #reset board state
        ChessController.clearBoard()   
        print(data)
        #if data is not correct, probably we are not in a game
        if(len(data)<3):
            return None
        global orientation
        global turn
        orientation = data[0]
        turn = data[1]
        moves = data[2]
        #recreates the game to reach the current board state
        for m in moves:  
            board.push_san(m)
        print(board)
        
        moveData=[0]
        #if its our turn
        if(orientation==turn):
            #lets ask the bot for the "best" move
            movimiento = bot.elegirMovimiento(board)
            if(movimiento[0]==-1): #bot error, probably we are not in a game 
                print ("NO ESTAMOS EN PARTIDA")
                return None
            #translates the bot move (d2d4) to the browser position (4244)
            moveData = ChessController.realizarMovimiento(movimiento[0].uci())
            print("move: " + str(movimiento[0]))
            print("Value: " + str(movimiento[1]))
        return moveData
        
    #translates the bot move (d2d4) to the browser position (4244)        
    def realizarMovimiento(selectedMove):    
        global orientation
        
        moveData = []
        startX = int(ord(selectedMove[0])-ord('a'))       
        startY = int(selectedMove[1])-1         
        endX = int(ord(selectedMove[2])-ord('a'))        
        endY = int(selectedMove[3])-1  
        
        #if black is below, position needs to be relative to H8 instead of A1
        if(orientation==False):
            startX = 7-startX
            endX = 7-endX
            startY = 7-startY
            endY = 7-endY
            
        moveData.append(startX)
        moveData.append(startY)
        moveData.append(endX)
        moveData.append(endY)
        if(len(selectedMove)>4): #if length > 4, we are promoting
            moveData.append(0) #just queen promotion suported, so we just append something
        return moveData