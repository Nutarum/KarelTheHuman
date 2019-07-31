# import libraries
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
from pynput.mouse import Button, Controller
import time
import random
    
class BrowserController:

    driver = None     
    cellSize = 0
    mouse = None 
    def initWeb():
        global driver
        global action
        
        #PARA QUE EL BOT COMIENZE LOGEADO EN LICHESS
        # Abrimos el navegador con normalidad, vamos a lichess.org y nos logeamos
        # Ahora iremos a C:/Users/<USUARIO>/AppData/Roaming/Mozilla/Firefox/Profiles
        # Una de las carpetas contendra la informacion de la sesion de firefox (cookies y demas)
        # En la ruta de la linea inferior, ponemos la ruta completa con el nombre de la carpeta
        fp = webdriver.FirefoxProfile('C:/Users/NutPc/AppData/Roaming/Mozilla/Firefox/Profiles/cxs6dg4g.default-release')        
        driver = webdriver.Firefox(fp)
        
        #PARA QUE EL NAVEGADOR NO SE MUESTRE
        #options = Options()
        #options.headless = True
        #driver = webdriver.Firefox(firefox_options=options)
        
        #driver = webdriver.Firefox()
        urlpage = 'https://lichess.org'
        # get web page
        driver.get(urlpage) 
        
    def initMouse():
        global mouse
        global boardStartX
        global boardStartY
        global rematchX
        global rematchY
        global squareSize
        mouse = Controller() 
        input("Move the mouse to the bottom left square and press any key...")
        boardStartX = mouse.position[0]
        boardStartY = mouse.position[1]
        input("Move the mouse to the bottom right square and press any key...")
        squareSize = (mouse.position[0]-boardStartX)/7
		    
    def aceptarDesafios():
        btn = driver.find_elements_by_xpath('/html/body/header/div[2]/div[2]/div/div/div/div[2]/form/button')
        for b in btn:
            b.click()
            
    def readState():    
        global driver
        global cellSize
        # find elements by xpath        
        data = []
        
        playing = driver.find_elements_by_xpath('/html/body/div[1]/main/aside/div/section/div[1]/div/div')
        for p in playing:
            if(not "Playing" in p.text):
                return [-1]
        
        orientation = driver.find_elements_by_xpath('/html/body/div[1]/main/div[1]/div[1]/div/cg-helper/cg-container/coords[1]')
        for o in orientation:
            #si las blancas estan abajo, el valor es "ranks" si las negras estan abajo "ranks black"
            data.append(o.get_attribute("className")=='ranks') 
        
        #vamos a leer el tamaño de las casillas
        #boardStart = driver.find_elements_by_xpath('/html/body/div[1]/main/div[1]/div[1]/div/cg-helper')
        #boardStart = boardStart[0]            
        #cellSize = int(boardStart.get_attribute("clientHeight"))
        
        #vamos a coger la tabla de movimientos
        moves = driver.find_elements_by_xpath('/html/body/div/main/div[1]/div/div[2]/m2')
        
        #segun el num de movimientos sabremos si es el turno de blancas o negras        
        data.append(len(moves)%2==0)
        movesArray = []
        for m in moves:                
            try:
                movesArray.append(m.text)
            except Exception as e:
                print(e)
        data.append(movesArray)
        return data
        
    def movePiece(moveData,dragMouseDelay):       
        global mouse
        global boardStartX
        global boardStartY
        global squareSize   
        currentX = int(boardStartX + (moveData[0]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        currentY = int(boardStartY - (moveData[1]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        mouse.position = (currentX, currentY)
        mouse.press(Button.left)
        #mouse.click(Button.left, 1)
        targetX = int(boardStartX + (moveData[2]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        targetY = int(boardStartY - (moveData[3]*squareSize) + (random.randint(0, int(squareSize/4))-squareSize/8))
        i=0
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