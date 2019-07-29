import numpy as np
import random
import chess
from karelthehuman import KarelTheHuman

class ChessController:
    board = chess.Board()
    
    def clearBoard():        
        global board        
        board = chess.Board()
        
    def updateBoardState(data):
        global board      
        ChessController.clearBoard()   
        print(data)
        if(len(data)<3):
            return
        global orientation
        global turn
        orientation = data[0]
        turn = data[1]
        moves = data[2]
        for m in moves:  
            board.push_san(m)
        print(board)
        
        moveData=[0]
        if(orientation==turn):
            movimiento = KarelTheHuman.elegirMovimiento(board)
            if(movimiento[0]==-1):            
                print ("NO ESTAMOS EN PARTIDA")
                return [-1]
            moveData = ChessController.realizarMovimiento(movimiento[0].uci())
            print("move: " + str(movimiento[0]))
            print("Value: " + str(movimiento[1]))
        return moveData
            
    def realizarMovimiento(selectedMove):    
        global orientation
        
        moveData = []
        startX = int(ord(selectedMove[0])-ord('a'))       
        startY = int(selectedMove[1])-1         
        endX = int(ord(selectedMove[2])-ord('a'))        
        endY = int(selectedMove[3])-1  
        
        if(orientation==False):
            startX = 7-startX
            endX = 7-endX
            startY = 7-startY
            endY = 7-endY
            
        moveData.append(startX)
        moveData.append(startY)
        moveData.append(endX)
        moveData.append(endY)
        if(len(selectedMove)>4): #si mide mas de 4 es que estamos coronando        
            moveData.append(0)
        return moveData