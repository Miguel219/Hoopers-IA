from Hoopers import Game

#Se inicializa el juego
game = Game()



ac = game.actions()
print(game.result(ac[0]))
print('-----------------------------')
for row in game.board:
    for square in row:
        print(square)
