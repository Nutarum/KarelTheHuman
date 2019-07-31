# Karel the human
Chess bot (working on lichess.org)

## Como ejecutar
Clone the repository
```
git clone https://gitlab.com/Nutarum/karelthehuman.git
```

Instalar python

Añadir dependencias
pip install python-chess
pip install pynput
pip install selenium
pip install colorama
(y tal vez tambien pip install beautifulsoup4???)

Tener mozilla firefox instalado

y ejecutar:
python main.py

navegar manualmente en lichess hasta la partida que quieras jugar
y marcar la casilla inferior izq y inferior derecha poniendo el raton encima
y pulsando una tecla (con el foco en la consola)

El bot ademas aceptara cualquier desafio de partida, siempre que no este ya jugando (hay que marcar previamente el lugar de las casillas inferior izq y inferior derecha)

### PARA QUE EL BOT COMIENZE LOGEADO EN LICHESS
Mirar instrucciones al inicio de la clase browserController.py

## Trainer
En la carpeta karelthetrainer tenemos un simulador para hacer duelos y pruebas entre diferentes versiones del bot.

## >>> ToDo <<<
- cuando la pantalla de lichess es muy pequeña peta, hacer que avise sin crashear
- hacer que detecte automaticamente la posición del tablero

## >>> BUGS <<<
- 

