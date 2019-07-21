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
        
        #PARA QUE EL NAVEGADOR NO SE MUESTRE
        #options = Options()
        #options.headless = True
        #driver = webdriver.Firefox(firefox_options=options)
        
        #PARA QUE EL NAVEGADOR SE MUESTRE
        driver = webdriver.Firefox()
        urlpage = 'https://lichess.org/tv'
        # get web page
        driver.get(urlpage) 
        
    def initMouse():
        global mouse
        global boardStartX
        global boardStartY
        global squareSize
        mouse = Controller() 
        input("Move the mouse to the bottom left square and press any key...")
        boardStartX = mouse.position[0]
        boardStartY = mouse.position[1]
        input("Move the mouse to the bottom right square and press any key...")
        squareSize = (mouse.position[0]-boardStartX)/7
        
    def readState():    
        global driver
        global cellSize
        # find elements by xpath        
        data = []
        
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
        
    def movePiece(moveData):       
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
            if(i%20==0):
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
        