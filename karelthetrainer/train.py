import numpy as np
import random
import chess
import chess.pgn
import collections

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
            print(board)    
            if(board.turn):
                print("\nWhite to move: " + str(botWhite))
                board.push(botWhite.elegirMovimiento(board))
            else:    
                print("\nBlack to move: " + str(botBlack))
                board.push(botBlack.elegirMovimiento(board))
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
    
Train.playGame()            