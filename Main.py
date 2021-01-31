from pandas import *
from Hoopers import Game, Coord

#Se inicializa el juego
game = Game()


print(DataFrame(game.board))

while (game.state < 2):
    print('-' * 40)
    if (game.state == 0):
        action = game.alphaBetaSearch()
        print('Acción:')
        print(action)
        game, path = game.result(action, calculatePath=True)
        print('Camino:')
        print(path)
    elif (game.state == 1):
        i = None
        f = None
        actions = game.actions()
        while (i,f) not in actions:
            i = Coord(
                int(input('Ingresa la coordenada x de la ficha a mover: ')), 
                int(input('Ingresa la coordenada y de la ficha a mover: '))) 
            f = Coord(
                int(input('Ingresa la coordenada x de la casilla destino: ')), 
                int(input('Ingresa la coordenada y de la casilla destino: '))) 
        print('-' * 40)
        print('Acción:')
        print((i,f))
        game, path = game.result((i,f), calculatePath=True)
        print('Camino:')
        print(path)

    #Se revisa si alguien ya gano
    if game.isFinished()[0]:
        print('Gano el jugador ' + str(game.isFinished()[1] + 1) + ' con ' + str(game.isFinished()[2]) + ' puntos')
        game.state = 2


    print(DataFrame(game.board))
