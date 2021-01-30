from Hoopers import Game, squaresToMove

#Se inicializa el juego
game = Game()

def toMove(game):
    if (game.state == 0):
        return game.player1
    elif (game.state == 1):
        return game.player2


def actions(game):
    #Tupla con todas las acciones
    availableActions = tuple()
        
    for piece in toMove(game):
        x, y = piece.getPosition()
        square = game.board[y - 1][x - 1]
        availableActions = squaresToMove(square.getPosition(), square, availableActions)
    
    return availableActions
    
def isTerminal(game):
    countPiecesOnEnemysCamp = utility(toMove(game))
    if (countPiecesOnEnemysCamp > (len(toMove(game)) / 2)):
        return True
    else:
        return False    

def utility(game, player):
    countPiecesOnEnemysCamp = 0
    for piece in player:
        x, y = piece.getPosition().x - 1, piece.getPosition().y - 1
        if (x + y < (game.dimension/2)):
            countPiecesOnEnemysCamp += 1
    return countPiecesOnEnemysCamp 



ac = actions(game)
print(game.moveToPath(toMove(game),ac[0][0],ac[0][1]))
print('-----------------------------')
for row in game.board:
    for square in row:
        print(square)
