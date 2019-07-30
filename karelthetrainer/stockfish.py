import chess
import chess.engine
import asyncio

class Stockfish: 
    engine = None    
    def __init__(self,skillLevel):
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish_10_x64.exe")  
        #print(engine.options) #para mostrar todas las opciones de config
        #print(engine.options["Skill Level"]) #para mostrar los valores de una opcion de config
        self.engine.configure({"Skill Level": skillLevel}) #entre 1 y 20 

    def elegirMovimiento(self,board):  
        #el depth tampoco es que haga mucho, lo importante es el skill level configurado al inicio de esta clase
        #result = engine.play(board, chess.engine.Limit(time=0.01,depth=1))  
        result = self.engine.play(board, chess.engine.Limit(time=0.01))             
        return [result.move,0]
        
        
        
    