import numpy as np
import random
import chess
import chess.pgn
import collections
from colorama import Fore, Back, Style, init
init()

from karelthehumanV1 import KarelTheHumanV1
from karelthehumanV2 import KarelTheHumanV2

class Train:        
    def playGame():     
        print("Starting...") 
        
        botWhite = KarelTheHumanV1
        botBlack = KarelTheHumanV2
        if (random.random() <= .5):
            tmp = botWhite
            botWhite=botBlack
            botBlack=tmp       
        
        board = chess.Board()
        while(not board.is_game_over()):              
            if(board.turn):
                mov = botWhite.elegirMovimiento(board)
            else:    
                mov = botBlack.elegirMovimiento(board)
            Train.printBoard(board,mov,botWhite,botBlack)  
            board.push(mov[0])
            input("")
        print("Game over")
        print(Train.board_to_game(board,botWhite,botBlack)) 
            
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
	
    def printBoard(board,mov,botWhite,botBlack):
        print()
        pieces = board.piece_map() #diccionario [casilla, pieza]
        print ("  -----------------")
        for i in range(7,-1,-1):
            print(" | ",end='')       
            for j in range(8):             
                casilla = (i*8)+j                
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