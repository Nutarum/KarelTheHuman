import chess
import chess.engine

class Stockfish: 
    engine = None    
    def __init__(self,skillLevel=20):
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish_10_x64.exe")  
        #print(engine.options) #para mostrar todas las opciones de config
        #print(engine.options["Skill Level"]) #para mostrar los valores de una opcion de config
        self.engine.configure({"Skill Level": skillLevel}) #entre 1 y 20 

    def elegirMovimiento(self,board):  
        #el depth tampoco es que haga mucho, lo importante es el skill level configurado al inicio de esta clase
        #result = engine.play(board, chess.engine.Limit(time=0.01,depth=1))  
        
        #no podemos usar el movimiento que hay en info['pv][0] 
        #porque aqui stockfish analiza siempre como si tubiese skill level 20
        #(por lo que el value que vemos será el de stockfish 20)
        info = self.engine.analyse(board,chess.engine.Limit(time=0.01)) 
        
        result = self.engine.play(board,chess.engine.Limit(time=0.01)) 
        return [result.move,info['score']]
        
        
        
    