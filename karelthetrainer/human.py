import random
import chess
from colorama import Fore, Back, Style, init
init()

class Human:
    def elegirMovimiento(board): 
        mov=[]
        if board.move_stack:
            mov = [board.peek(),0]
        Human.printBoard(board,mov)
        
        salir = False
        while(not salir):
            mov = input("Introduce movimiento (uci notation): ")    
            try:
                mov = chess.Move.from_uci(mov)
                if(mov in board.legal_moves):
                    salir = True
                else:
                    print("Movimiento ilegal.")
            except:                
                print("Movimiento incorrecto.")
                
            
        return [mov,0]
        
    #dibuja el tablero, remarcando el movimiento elegido por el bot
    #ademas de escribir el valor que le da al bot al tablero tras el movimiento
    def printBoard(board,mov):
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
                    Human.printPiece(pieces[casilla])
                else:
                    print(". ",end='')
                print(Back.BLACK,end='') 
            print("| " + (str(i+1)))        
        print ("  -----------------")
        print ("   a b c d e f g h")        
           
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