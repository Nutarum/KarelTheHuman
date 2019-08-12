# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from pynput.mouse import Button, Controller
import time
import random
import os

boardStartX = -1
boardStartY = -1
squareSize = 0
mouse = Controller()

class BrowserController:

    driver = None     
    
    mouse = None 
    def initWeb(firefoxProfileFolder):
        global driver
        global action
        
        #PARA QUE EL BOT COMIENZE LOGEADO EN LICHESS
        # Abrimos el navegador con normalidad, vamos a lichess.org y nos logeamos
        # Ahora iremos a C:/Users/<USUARIO>/AppData/Roaming/Mozilla/Firefox/Profiles
        # Una de las carpetas contendra la informacion de la sesion de firefox (cookies y demas)
        # En el fichero config.txt, en la linea que sigue a "folder of mozilla firefox profile"
        # Pondremos el nombre de la carpeta
        # * SI NO SALTA EL ERROR DE QUE NO NOS LOGEAREMOS AL INCIAR LA APP, 
        #   PERO AUN ASI NO NOS LOGEAMOS, EN FIREFOX->OPCIONES->PRIVACIDAD Y SEGURIDAD
        #   HISTORIAL (al lado de "limpiar el historial cuando firefox se cierre") pulsamos el boton configuracion...
        #   y desmarcamos todas las casillas
        
        try:
            fp = webdriver.FirefoxProfile(os.getenv('APPDATA') + '/Mozilla/Firefox/Profiles/' + firefoxProfileFolder)        
            driver = webdriver.Firefox(fp)
        except Exception as e:
            print("ARCHIVO DE SESION DE FIREFOX NO ENCONTRADO, EL BOT NO ESTARÁ LOGEADO")
            print(e)
            driver = webdriver.Firefox()
        
        urlpage = 'https://lichess.org'
        # opens the browser
        driver.get(urlpage) 
        
        # Resize the window to the screen width/height
        driver.set_window_size(800, 600)
        # Move the window to position x/y
        driver.set_window_position(0, 0)
    
    #loads the absolute position of the bottom left corner of the board in the screen, and the size of the board squares
    def loadBoardPosition():
        global squareSize
        global boardStartX
        global boardStartY  
        global driver
        
        #we get the browser upper menu height, so we know where the browser content starts exactly
        barraSuperior = driver.execute_script('return window.outerHeight - window.innerHeight;')
        
        files = driver.find_elements_by_xpath('/html/body/div[1]/main/div[1]/div[1]/div/cg-helper/cg-container/coords[2]')
        ranks = driver.find_elements_by_xpath('/html/body/div[1]/main/div[1]/div[1]/div/cg-helper/cg-container/coords[1]')
        for f in files:
            boardStartX = f.location['x']
            boardStartY = f.location['y'] + barraSuperior
        for r in ranks:            
            squareSize = (r.location['x']+r.size['width']-boardStartX)/8
            
        boardStartX = boardStartX + squareSize/2
        boardStartY = boardStartY - squareSize/2
    
    #if we have any pending challenge, the bot will accept it
    def aceptarDesafios():
        btn = driver.find_elements_by_xpath('/html/body/header/div[2]/div[2]/div/div/div/div[2]/form/button')
        for b in btn:
            b.click()
    
    #reads the browser content, to return the current game state
    #returns [bool,bool,list(String)] [board orientation, whos next to move, (d4,Nc6.....)]
    def readState():    
        global driver
        # find elements by xpath        
        data = []
        
        #detects if we are currently in a game
        playing = driver.find_elements_by_xpath('/html/body/div[1]/main/aside/div/section/div[1]/div/div')
        for p in playing:
            if(not "Playing" in p.text and not "Jugando" in p.text):
                return [-1] #if not in a game
        
        #we get the board orientation (relevant to know what color we are playing, and to calculate the board coordinates
        orientation = driver.find_elements_by_xpath('/html/body/div[1]/main/div[1]/div[1]/div/cg-helper/cg-container/coords[1]')
        for o in orientation:
            #if white pieces are below, classname=="ranks", otherwise it will be "ranks black"
            data.append(o.get_attribute("className")=='ranks')    
        
        #the table with all the game moves
        moves = driver.find_elements_by_xpath('/html/body/div/main/div[1]/div/div[2]/m2')
        
        #if move count is even, its white to move, otherwise, its blacks turn       
        data.append(len(moves)%2==0)
        #now we just append all the moves
        movesArray = []
        for m in moves:                
            try:
                movesArray.append(m.text)
            except Exception as e:
                print(e)
        data.append(movesArray)
        return data
    
    #recieves the board coordinates (d2d4 will be 4244) and perform the move with the mouse
    #(coordinates are relative to the bottom left corner (bottom left DOESNT NEED TO BE A1, can also be H8))    
    def movePiece(moveData,dragMouseDelay):       
        global mouse
        global boardStartX
        global boardStartY
        global squareSize 
        if(boardStartX==-1):
            BrowserController.loadBoardPosition()
                
        currentX = int(boardStartX + (moveData[0]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        currentY = int(boardStartY - (moveData[1]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        mouse.position = (currentX, currentY)
        mouse.press(Button.left)
        #mouse.click(Button.left, 1)
        targetX = int(boardStartX + (moveData[2]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        targetY = int(boardStartY - (moveData[3]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        i=0
        #we drag the mouse, trying to simulate "human" behavior (maybe not that human LUL)
        while(currentX!=targetX or currentY!=targetY):
            i=i+1
            if(i%dragMouseDelay==0):
                time.sleep(0.001)
            if(currentX!=targetX and currentY!=targetY):
                a = random.randint(0, 100)
                if(a<50):
                    if(currentX<targetX):
                        currentX = currentX+1
                    else:
                        currentX = currentX-1
                else:
                    if(currentY<targetY):
                        currentY = currentY+1
                    else:
                        currentY = currentY-1
            else:
                if(currentX!=targetX):
                    if(currentX<targetX):
                        currentX = currentX+1
                    else:
                        currentX = currentX-1
                else:
                    if(currentY<targetY):
                        currentY = currentY+1
                    else:
                        currentY = currentY-1
            mouse.position = (currentX,currentY)
        #mouse.click(Button.left, 1)
        mouse.release(Button.left)
        if(len(moveData)==5):
            time.sleep(0.1)
            mouse.click(Button.left, 1)