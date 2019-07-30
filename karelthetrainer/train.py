import numpy as np
import random
import chess
import chess.pgn
import collections
from colorama import Fore, Back, Style, init
init()

from stockfish import Stockfish
from karelthehumanV1 import KarelTheHumanV1
from karelthehumanV2 import KarelTheHumanV2

class Train:        
    def playGame():     
        print("Starting...") 
        #preguntamos al usuario si queremos mostrar los movimientos 
        #de la partida, y pedir un input entre cada movimiento
        simulacionRapida = int(input("Simulación rápida(1/0):"))
        if(simulacionRapida!=0 and simulacionRapida!=1):
            simulacionRapida=0
        if(simulacionRapida==1):
            #si elegimos simulacionRapida (solo muestra resultados al acabar cada partida)
            #preguntamos cuantas partidas queremos simular
            numPartidas = int(input("Número de partidas:"))
        else:
            numPartidas = 1
        
        bot1 = Stockfish(1) #recibe como parametro el nivel de stockfish (de 1 a 20)
        bot2 = KarelTheHumanV1
        victoriasBot1 = 0
        victoriasBot2 = 0
        empates = 0
               
        #mientras queden partidas por jugar
        while(numPartidas>0):
            #randomizamos que bot juega con blancas y cual con negras
            botWhite = bot1
            botBlack = bot2
            if (random.random() <= .5):
                tmp = botWhite
                botWhite=botBlack
                botBlack=tmp   
            #inicializamos la partida
            board = chess.Board()
            #mientras no se acabe la partida
            while(not board.is_game_over()):   
                #pedimos el movimiento al bot que le toque mover
                if(board.turn):
                    mov = botWhite.elegirMovimiento(board)
                else:    
                    mov = botBlack.elegirMovimiento(board)
                #si no estamos en simulacionRapida dibujamos el estado del tablero
                if(simulacionRapida==0):
                    Train.printBoard(board,mov,botWhite,botBlack)
                    input("")
                #realizamos el movimiento    
                board.push(mov[0])
            
            print("Game over")
            #si estamos en simulacionRapida mostramos el tablero
            #en caso contrario ya se habra mostrado antes del ult movimiento
            if(simulacionRapida==1):
                Train.printBoard(board,[],botWhite,botBlack)
            #mostramos toda la partida en formato CGN
            print(Train.board_to_game(board,botWhite,botBlack))
            numPartidas = numPartidas-1
            print("Partidas restantes: " + str(numPartidas))
            #vamos contando el numero de victorias para cada bot
            if(board.result()=="1-0"):
                if(bot1==botWhite):
                    victoriasBot1 = victoriasBot1+1
                else:
                    victoriasBot2 = victoriasBot2+1
            elif(board.result()=="0-1"):
                if(bot1==botWhite):
                    victoriasBot2 = victoriasBot2+1
                else:
                    victoriasBot1 = victoriasBot1+1
            elif(board.result()=="1/2-1/2"):
                empates = empates+1
            else:
                input("ERROR, PARTIDA CON RESULTADO INDETERMINADO")
        #mostramos los resultados finales
        print()
        print("Victorias " + str(bot1) + ": " + str(victoriasBot1))
        print("Victorias " + str(bot2) + ": " + str(victoriasBot2))
        print("Empates " + str(empates))
        
    #funcion necesaria para luego mostrar la partida en notacion CGN
    def board_to_game(board,botWhite,botBlack):
        game = chess.pgn.Game()
        # Undo all moves.
        switchyard = collections.deque()
        while board.move_stack:
            switchyard.append(board.pop())
        game.setup(board)
        node = game
        # Replay all moves.
        while switchyard:
            move = switchyard.pop()
            node = node.add_variation(move)
            board.push(move)
        game.headers["White"] = botWhite
        game.headers["Black"] = botBlack
        game.headers["Result"] = board.result()
        return game
	
    #dibuja el tablero, remarcando el movimiento elegido por el bot
    #ademas de escribir el valor que le da al bot al tablero tras el movimiento
    def printBoard(board,mov,botWhite,botBlack):
        print()
        pieces = board.piece_map() #diccionario [casilla, pieza]
        print ("  -----------------")
        #vamos a recorrer cada casilla del tablero
        for i in range(7,-1,-1):
            print(" | ",end='')       
            for j in range(8):             
                casilla = (i*8)+j #la notacion de las casillas son los numeros del 0 al 63       
                #mov tendrá tamaño 0 cuando la partida ya ha acabado
                if(len(mov)>0):
                    #si hay que remarcar la casilla (por ser parte del proximo movimiento)
                    if(casilla==mov[0].from_square):
                        print(Back.CYAN,end='') 
                    elif(casilla==mov[0].to_square):
                        print(Back.YELLOW,end='') 
                #si hay una pieza en esta casilla
                if(casilla in pieces.keys()): 
                    Train.printPiece(pieces[casilla])
                else:
                    print(". ",end='')
                print(Back.BLACK,end='') 
            print("| " + (str(i+1)))        
        print ("  -----------------")
        print ("   a b c d e f g h")
        
        #mostramos a quien lo toca mover, ademas del
        #proximo movimiento y el valor del tablero tras el
        if(len(mov)>0):
            if(board.turn):
                print("\nWhite to move: " + str(botWhite))
            else:    
                print("\nBlack to move: " + str(botBlack))
            print("Move: " + str(mov[0]))
            print("Value: " + str(mov[1])+"\n")
    
    def printPiece(piece):
        char = 'x'
        if(piece.piece_type==1):
            char = 'p'
        elif(piece.piece_type==2):
            char = 'n'
        elif(piece.piece_type==3):
            char = 'b'
        elif(piece.piece_type==4):
            char = 'r'
        elif(piece.piece_type==5):
            char = 'q'
        elif(piece.piece_type==6):
            char = 'k'
        if(piece.color):
            char = char.upper()
        print(char + ' ',end='')    
Train.playGame()            