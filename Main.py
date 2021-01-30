from Hoopers import Game, squaresToMove

#Se inicializa el juego
game = Game()
state = 0

def toMove(state):
    if (state == 0):
        return game.player1
    elif (state == 1):
        return game.player2


def actions(state):
    #Tupla con todas las acciones
    availableActions = tuple()
        
    for piece in toMove(state):
        x, y = piece.getPosition()
        square = game.board[y - 1][x - 1]
        availableActions = squaresToMove(square.getPosition(), square, availableActions)
    
    return availableActions
    
def isTerminal(state):
    countPiecesOnEnemysCamp = utility(toMove(state))
    if (countPiecesOnEnemysCamp > (len(toMove(state)) / 2)):
        return True
    else:
        return False    

def utility(state, player):
    countPiecesOnEnemysCamp = 0
    for piece in player:
        x, y = piece.getPosition().x - 1, piece.getPosition().y - 1
        if (x + y < (game.dimension/2)):
            countPiecesOnEnemysCamp += 1
    return countPiecesOnEnemysCamp 



ac = actions(state)
print(game.moveToPath(toMove(state),ac[0][0],ac[0][1]))
print('-----------------------------')
for row in game.board:
    for square in row:
        print(square)