from pandas import *
import numpy as np
from Hoopers import Game, Coord

#Se inicializa el juego
game = Game()

#Tipo de jugabilidad
typeToPlay = 0

while typeToPlay == 0:
    string = input('Si quieres jugar contra el programa ingresa 1, si quieres que el programa se enfrente a si mismo ingresa 2: ')
    try:
        integer = int(string)
        if integer == 1 or integer == 2:
            typeToPlay = integer
        else:
            print('Ingresa una acción correcta')
    except:
        print('Ingresa una acción correcta')


dataFrame = DataFrame(game.board)
dataFrame.index = np.arange(1,len(dataFrame)+1)
dataFrame.columns = np.arange(1,len(dataFrame)+1)
print(dataFrame)

while (game.state < 2):
    print('-' * 40)
    print('Jugador ' + str(game.state + 1) + ':')
    if (game.state == 0):
        action = game.alphaBetaSearch()
        print('Acción:')
        print(action)
        game, path = game.result(action, calculatePath=True)
        print('Camino:')
        print(path)
    elif (game.state == 1):
        if typeToPlay == 1:
            i = None
            f = None
            actions = game.actions()
            while (i,f) not in actions:
                try:
                    i = Coord(
                        int(input('Ingresa la coordenada x de la ficha a mover: ')), 
                        int(input('Ingresa la coordenada y de la ficha a mover: '))) 
                    f = Coord(
                        int(input('Ingresa la coordenada x de la casilla destino: ')), 
                        int(input('Ingresa la coordenada y de la casilla destino: ')))
                    if (i,f) not in actions:
                        print('La acción ingresada no es correcta')
                except:
                    print('La acción ingresada no es correcta')    
            print('-' * 40)
            print('Acción:')
            print((i,f))
            game, path = game.result((i,f), calculatePath=True)
            print('Camino:')
            print(path)
        else:
            action = game.alphaBetaSearch2()
            print('Acción:')
            print(action)
            game, path = game.result(action, calculatePath=True)
            print('Camino:')
            print(path)

    #Se revisa si alguien ya gano
    if game.isFinished()[0]:
        print('Gano el jugador ' + str(game.isFinished()[1] + 1) + ' con ' + str(game.isFinished()[2]) + ' puntos')
        game.state = 2


    dataFrame = DataFrame(game.board)
    dataFrame.index = np.arange(1,len(dataFrame)+1)
    dataFrame.columns = np.arange(1,len(dataFrame)+1)
    print(dataFrame)

