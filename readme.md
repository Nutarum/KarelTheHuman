# Karel the human
Chess bot (working on lichess.org)

## Como ejecutar
Clone the repository
```
git clone https://gitlab.com/Nutarum/karelthehuman.git
```

Instalar python

Añadir dependencias <br />
&nbsp;&nbsp;&nbsp;&nbsp; - pip install python-chess <br />
&nbsp;&nbsp;&nbsp;&nbsp; - pip install pynput <br />
&nbsp;&nbsp;&nbsp;&nbsp; - pip install selenium <br />
&nbsp;&nbsp;&nbsp;&nbsp; - pip install colorama <br />
&nbsp;&nbsp;&nbsp;&nbsp; - (y tal vez tambien pip install beautifulsoup4???)

Tener mozilla firefox instalado

y ejecutar:
python main.py

navegar manualmente en lichess hasta la partida que quieras jugar
y marcar la casilla inferior izq y inferior derecha poniendo el raton encima
y pulsando una tecla (con el foco en la consola)

El bot ademas aceptara cualquier desafio de partida (si realizamos los pasos para que comienze logeado en lichess), siempre que no este ya jugando (hay que marcar previamente el lugar de las casillas inferior izq y inferior derecha)

### PARA QUE EL BOT COMIENZE LOGEADO EN LICHESS
Mirar instrucciones al inicio de la clase browserController.py

### PARA USAR LAS DISTINTAS VERSIÓN DEL BOT
En el archivo chessController.py
modificar la linea "from karelthetrainer.karelthehumanV2 import KarelTheHumanV2 as KarelTheHuman"
por el bot deseado, por ejemplo "from karelthetrainer.stockfish import Stockfish as KarelTheHuman"

## Trainer
En la carpeta karelthetrainer tenemos un simulador para hacer duelos y pruebas entre diferentes versiones del bot.

### Idioma de lichess
El bot solo detectara estar en partida si tenemos lichess en español o ingles <br />
debido a esta linea en browserController "if(not "Playing" in p.text and not "Jugando" in p.text):"

## >>> ToDo <<<
- cuando la pantalla de lichess es muy pequeña peta, hacer que avise sin crashear
- hacer que detecte automaticamente la posición del tablero

## >>> BUGS <<<
- 

