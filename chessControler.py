import numpy as np
import random
import chess

class ChessControler:
    board = chess.Board()
    
    def clearBoard():        
        global board        
        board = chess.Board()
        
    def updateBoardState(data):
        global board      
        ChessControler.clearBoard()   
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
            movimiento = ChessControler.elegirMovimiento()
            moveData = ChessControler.realizarMovimiento(movimiento)
        else:
            print("\nValue: " + str(ChessControler.getBoardValue())+"\n")
        return moveData
        
    def elegirMovimiento():
        global board
        global orientation
        
        moveList = list(board.legal_moves)     
        
        bestValue = -99999
        
        for i in range(0,len(moveList)):
            board.push(moveList[i])            
            value = ChessControler.getBoardValue()
            if(value>bestValue):
                bestValue=value
                bestMove=i            
            board.pop()      
        print("\nMove: " + str(moveList[bestMove]) + "\n")
        print("Value: " + str(bestValue)+"\n")
        return moveList[bestMove].uci()
        
    def getBoardValue():
        global board
        #value = random.randint(0, 1000)
        value = 0
        pieces = board.piece_map() #diccionario [casilla, pieza]
        for i in range(64):
            if(board.is_attacked_by(orientation,i)):
                value = value + 0.1
        for p in pieces: #en p tenemos la casilla
            piece = pieces[p]
            pieceValue =  ChessControler.getPieceValue(piece.piece_type)
            if(piece.color == orientation): #si la pieza es de nuestro color
                value = value + pieceValue
                atacantes = board.attackers(not piece.color, p)
                minAtacante = 99
                for a in atacantes:
                    aValue = ChessControler.getPieceValue(board.piece_at(a).piece_type)
                    if(aValue < minAtacante):
                        minAtacante = aValue
                defensores = board.attackers(piece.color, p)
                minDefensor = 99
                for d in defensores:
                    dValue = ChessControler.getPieceValue(board.piece_at(d).piece_type)
                    if(dValue < minAtacante):
                        minDefensor = dValue    
                if(minDefensor==99):
                    if(minAtacante<minDefensor): #si una pieza esta atacada pero no defendida
                        value = value - (pieceValue/2)
                else:             
                    if(minAtacante<pieceValue): #si una pieza esta atacada por una de menor valor que ella
                        value = value - ((pieceValue-minAtacante)/2)

            else:
                value = value - pieceValue
                atacantes = board.attackers(not piece.color, p)
                minAtacante = 99
                for a in atacantes:
                    aValue = ChessControler.getPieceValue(board.piece_at(a).piece_type)
                    if(aValue < minAtacante):
                        minAtacante = aValue
                defensores = board.attackers(piece.color, p)
                minDefensor = 99
                for d in defensores:
                    dValue = ChessControler.getPieceValue(board.piece_at(d).piece_type)
                    if(dValue < minAtacante):
                        minDefensor = dValue    
                if(minDefensor==99):
                    if(minAtacante<minDefensor): #si una pieza esta atacada pero no defendida
                        value = value - (pieceValue/2)
                else:             
                    if(minAtacante<pieceValue): #si una pieza esta atacada por una de menor valor que ella
                        value = value - ((pieceValue-minAtacante)/2)
        return value 

    def getPieceValue(piece_type):
        if(piece_type==1):
            return 1
        elif(piece_type==2):
            return 3
        elif(piece_type==3):
            return 3
        elif(piece_type==4):
            return 5
        elif(piece_type==5):
            return 9   
        elif(piece_type==6):
            return 10
        
            
        
    
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
        return moveData