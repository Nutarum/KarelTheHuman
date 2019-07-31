import random
import chess

# Esta versión del bot se basa en darle un valor a la posción del tablero 
# tras cada movimiento posibles, y realizar el movimiento con mejor valor

# la evaluación se basa en evaluar todos los movimientos posibles del rival
# tras cada movimiento propio, y quedarnos con el mejor

# elegiremos el movimiento propio que da como resultado el menor valor
# es decir, el peor de los mejores movimientos del rival

# * La evaluación del tablero tras los movimientos del rival
#   es identica a la evaluación del tablero de karelthehumanV1

CELL_CONTROLED_VALUE = 0.07
UNDEFENDED_VALUE_MULTI = 0.7
ATTACKED_VALUE_MULTI = 0.1
RANDOM_RANGE = 0

class KarelTheHuman:
    def elegirMovimiento(board):        
        moveList = list(board.legal_moves)     
        
        if(len(moveList)==0):
            return -1
        bestValue = 99999
        bestMove = 0
                
        for i in range(0,len(moveList)):
            board.push(moveList[i])       
            if(board.is_checkmate()):
                bestValue=99999
                bestMove=i
                board.pop()
                break
                
            #listValues.append(KarelTheHuman.getBoardValue(board))                        
            
            moveList2 = list(board.legal_moves)    
            
            bestValue2 = -9999999   
            
            #si un movimiento es un empate por ahogado no lo hara
            #a no ser que ningun otro movimiento tenga valoracion positiva
            if(len(moveList2)==0): 
                bestValue2 = 0           
                     
            for j in range(0,len(moveList2)):
                board.push(moveList2[j])   
                value2 = KarelTheHuman.getBoardValue(board)
                if(value2>bestValue2):
                    bestValue2=value2
                board.pop()
            
            if(bestValue2<bestValue):
                bestValue=bestValue2
                bestMove=i
            board.pop()        
            
        ret = []
        ret.append(moveList[bestMove])
        ret.append(bestValue)
        
        return ret
        
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
                value = value + CELL_CONTROLED_VALUE
        for p in pieces: #en p tenemos la casilla
            piece = pieces[p]
            pieceValue =  KarelTheHuman.getPieceValue(piece,p)
            if(piece.color == orientation): #si la pieza es de nuestro color
                value = value + pieceValue
                
                atacantes = board.attackers(not piece.color, p)
                minAtacante = 99
                for a in atacantes:
                    aValue = KarelTheHuman.getPieceValue(board.piece_at(a),a)
                    if(aValue < minAtacante):
                        minAtacante = aValue
                defensores = board.attackers(piece.color, p)
                minDefensor = 99
                for d in defensores:
                    dValue = KarelTheHuman.getPieceValue(board.piece_at(d),d)
                    if(dValue < minAtacante):
                        minDefensor = dValue    
                if(minDefensor==99):
                    if(minAtacante<minDefensor): #si una pieza esta atacada pero no defendida
                        value = value - (pieceValue*UNDEFENDED_VALUE_MULTI)
                else:             
                    if(minAtacante<pieceValue): #si una pieza esta atacada por una de menor valor que ella
                        value = value - ((pieceValue-minAtacante)*UNDEFENDED_VALUE_MULTI)

            else: #si la pieza es del rival
                value = value - pieceValue
                
                atacantes = board.attackers(not piece.color, p)
                minAtacante = 99
                for a in atacantes:
                    aValue = KarelTheHuman.getPieceValue(board.piece_at(a),a)
                    if(aValue < minAtacante):
                        minAtacante = aValue
                defensores = board.attackers(piece.color, p)
                minDefensor = 99
                for d in defensores:
                    dValue = KarelTheHuman.getPieceValue(board.piece_at(d),d)
                    if(dValue < minAtacante):
                        minDefensor = dValue                       
                if(minDefensor==99):
                    if(minAtacante<minDefensor): #si una pieza esta atacada pero no defendida
                        valueAtaques = valueAtaques + pieceValue
                else:             
                    if(minAtacante<pieceValue): #si una pieza esta atacada por una de menor valor que ella
                        valueAtaques = valueAtaques + pieceValue-minAtacante
                        
        valueAtaques = valueAtaques * ATTACKED_VALUE_MULTI
        
        # si un movimiento del rival nos puede empatar, le damos un valor positivo
        # para que no nos guste la opción
        if(board.can_claim_threefold_repetition()):
            return 10
        #si este movimiento produce un ahogado
        if(len(movPosiblesRival)==0):
            return 10
            
        if(value>12): 
            #ademas, vamos a intentar evitar que el rival haga movimientos
            #que limiten mucho nuestros movimientos posibles, si el rival va ganando
            if(len(movPosiblesRival)<10):
                value = value +0.5
            if(len(movPosiblesRival)<5):
                value = value +1
            if(len(movPosiblesRival)<3):
                value = value +1.5
            if(len(movPosiblesRival)<2):
                value = value +2
        value = value + valueAtaques
        return value + (random.random()*RANDOM_RANGE)
        

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