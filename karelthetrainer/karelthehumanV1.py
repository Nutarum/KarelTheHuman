import numpy as np
import random
import chess
import chess.pgn
import collections

class KarelTheHumanV1:
    def elegirMovimiento(board):        
        moveList = list(board.legal_moves)     
        
        if(len(moveList)==0):
            return -1
        bestValue = -99999
        bestMove = 0
        for i in range(0,len(moveList)):
            board.push(moveList[i])            
            value = KarelTheHumanV1.getBoardValue(board)
            if(value>bestValue):
                bestValue=value
                bestMove=i            
            board.pop()      
        print("\nMove: " + str(moveList[bestMove]) + "\n")
        print("Value: " + str(bestValue)+"\n")
        return moveList[bestMove]
        
    def getBoardValue(board):
        #tenemos que poner el turno negado, porque en este punto ya hemos pusheado nuestro movimiento para probarlo
        orientation = not board.turn 
    
        movPosiblesRival = list(board.legal_moves)  
        if(board.is_checkmate()):
            return 99999       
        #value = random.randint(0, 1000)
        value = 0
        valueAtaques = 0
        pieces = board.piece_map() #diccionario [casilla, pieza]
        for i in range(64):
            if(board.is_attacked_by(orientation,i)):
                value = value + 0.07
        for p in pieces: #en p tenemos la casilla
            piece = pieces[p]
            pieceValue =  KarelTheHumanV1.getPieceValue(piece,p)
            if(piece.color == orientation): #si la pieza es de nuestro color
                value = value + pieceValue
                
                atacantes = board.attackers(not piece.color, p)
                minAtacante = 99
                for a in atacantes:
                    aValue = KarelTheHumanV1.getPieceValue(board.piece_at(a),a)
                    if(aValue < minAtacante):
                        minAtacante = aValue
                defensores = board.attackers(piece.color, p)
                minDefensor = 99
                for d in defensores:
                    dValue = KarelTheHumanV1.getPieceValue(board.piece_at(d),d)
                    if(dValue < minAtacante):
                        minDefensor = dValue    
                if(minDefensor==99):
                    if(minAtacante<minDefensor): #si una pieza esta atacada pero no defendida
                        value = value - (pieceValue*0.7)
                else:             
                    if(minAtacante<pieceValue): #si una pieza esta atacada por una de menor valor que ella
                        value = value - ((pieceValue-minAtacante)*0.7)

            else: #si la pieza es del rival
                value = value - pieceValue
                
                atacantes = board.attackers(not piece.color, p)
                minAtacante = 99
                for a in atacantes:
                    aValue = KarelTheHumanV1.getPieceValue(board.piece_at(a),a)
                    if(aValue < minAtacante):
                        minAtacante = aValue
                defensores = board.attackers(piece.color, p)
                minDefensor = 99
                for d in defensores:
                    dValue = KarelTheHumanV1.getPieceValue(board.piece_at(d),d)
                    if(dValue < minAtacante):
                        minDefensor = dValue                       
                if(minDefensor==99):
                    if(minAtacante<minDefensor): #si una pieza esta atacada pero no defendida
                        valueAtaques = valueAtaques + pieceValue
                else:             
                    if(minAtacante<pieceValue): #si una pieza esta atacada por una de menor valor que ella
                        valueAtaques = valueAtaques + pieceValue-minAtacante
                        
        valueAtaques = valueAtaques * 0.1
        if(value + (valueAtaques * 0.1)>6): #si vamos ganando por mucho, vamos a ser mas agresivos
            valueAtaques = valueAtaques * 1.5
            if(board.can_claim_threefold_repetition()):
                return -1 #no queremos permitir empate por repetición cuando vamos ganando
            if(len(movPosiblesRival)==0):
                return -1 #si hemos ahogado (porque el mate ya habria hecho return
        if(value + (valueAtaques * 0.1)>12): #si vamos ganando por mucho, vamos a ser mas agresivos
            valueAtaques = valueAtaques * 1.5    
            #ademas, vamos a intentar hacer que el rival tenga el minimo número de movimientos posibles
            #lo que deberia hacer mas probable llegar a un mate
            if(len(movPosiblesRival)<10):
                value = value +0.5
            if(len(movPosiblesRival)<5):
                value = value +1
            if(len(movPosiblesRival)<3):
                value = value +1.5
            if(len(movPosiblesRival)<2):
                value = value +2
        value = value + valueAtaques
        return value 
        

    def getPieceValue(piece,pos):
        piece_type = piece.piece_type
        if(piece_type==1):
            #vamos a hacer que los peones valgan mas conforme mas hayan avanzado
            rank = chess.square_rank(pos)
            if(piece.color): #si somos blancas
                if(rank==3):
                    return 1.1
                elif(rank==4):
                    return 1.2
                elif(rank==5):
                    return 1.3
                elif(rank==6):
                    return 1.8
                elif(rank==7):
                    return 2.7
            else: #si somos negras                      
                if(rank==6):
                    return 1.1
                elif(rank==5):
                    return 1.2
                elif(rank==4):
                    return 1.3
                elif(rank==3):
                    return 1.8
                elif(rank==2):
                    return 2.7
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
            return 2      