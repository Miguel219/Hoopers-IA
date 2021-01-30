from Hoopers import Game

#Se inicializa el juego
game = Game()
state = 0

def toMove(state):
    if (state == 1):
        game.player1
    else:
        game.player2


def actions(state):
    
    availableActions = tuple()

    if (state == 0):
        for piece in game.player1:
            x, y = piece.getPosition()
            square = game.board[y - 1][x - 1]
            availableActions = squaresToMove(square, availableActions)
        for i in availableActions:
            print(i)
    elif (state == 1):
        for piece in game.player2:
            x, y = piece.getPosition()
            square = game.board[y - 1][x - 1]
            availableActions = squaresToMove(square, availableActions)

def squaresToMove(square, availableActions, recursive = False):
    #Revisa movimiento y salto a la izquierda
    if (square.getLeft()):
        if (square.getLeft().visitor):
            if (square.getHopLeft() and square.getHopLeft().visitor is None and square.getHopLeft().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopLeft().getPosition(),)
                availableActions = squaresToMove(square.getHopLeft(), availableActions, recursive=True)
        elif(square.getLeft().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getLeft().getPosition(),)

    #Revisa movimiento y salto a la derecha
    if (square.getRight()):
        if (square.getRight().visitor):
            if (square.getHopRight() and square.getHopRight().visitor is None and square.getHopRight().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopRight().getPosition(),)
                availableActions = squaresToMove(square.getHopRight(), availableActions, recursive=True)
        elif(square.getRight().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getRight().getPosition(),)

    #Revisa movimiento y salto hacia abajo
    if (square.getDown()):
        if (square.getDown().visitor):
            if (square.getHopDown() and square.getHopDown().visitor is None and square.getHopDown().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopDown().getPosition(),)
                availableActions = squaresToMove(square.getHopDown(), availableActions, recursive=True)
        elif(square.getDown().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getDown().getPosition(),)

    #Revisa movimiento y salto hacia arriba
    if (square.getUp()):
        if (square.getUp().visitor):
            if (square.getHopUp() and square.getHopUp().visitor is None and square.getHopUp().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopUp().getPosition(),)
                availableActions = squaresToMove(square.getHopUp(), availableActions, recursive=True)
        elif(square.getUp().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getUp().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal izquierda abajo
    if (square.getLeftDownDiagonal()):
        if (square.getLeftDownDiagonal().visitor):
            if (square.getHopLeftDownDiagonal() and square.getHopLeftDownDiagonal().visitor is None and square.getHopLeftDownDiagonal().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopLeftDownDiagonal().getPosition(),)
                availableActions = squaresToMove(square.getHopLeftDownDiagonal(), availableActions, recursive=True)
        elif(square.getLeftDownDiagonal().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getLeftDownDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal derecha abajo
    if (square.getRightDownDiagonal()):
        if (square.getRightDownDiagonal().visitor):
            if (square.getHopRightDownDiagonal() and square.getHopRightDownDiagonal().visitor is None and square.getHopRightDownDiagonal().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopRightDownDiagonal().getPosition(),)
                availableActions = squaresToMove(square.getHopRightDownDiagonal(), availableActions, recursive=True)
        elif(square.getRightDownDiagonal().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getRightDownDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal izquierda arriba
    if (square.getLeftUpDiagonal()):
        if (square.getLeftUpDiagonal().visitor):
            if (square.getHopLeftUpDiagonal() and square.getHopLeftUpDiagonal().visitor is None and square.getHopLeftUpDiagonal().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopLeftUpDiagonal().getPosition(),)
                availableActions = squaresToMove(square.getHopLeftUpDiagonal(), availableActions, recursive=True)
        elif(square.getLeftUpDiagonal().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getLeftUpDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal derecha arriba
    if (square.getRightUpDiagonal()):
        if (square.getRightUpDiagonal().visitor):
            if (square.getHopRightUpDiagonal() and square.getHopRightUpDiagonal().visitor is None and square.getHopRightUpDiagonal().getPosition() not in availableActions):
                availableActions = availableActions + (square.getHopRightUpDiagonal().getPosition(),)
                availableActions = squaresToMove(square.getHopRightUpDiagonal(), availableActions, recursive=True)
        elif(square.getRightUpDiagonal().getPosition() not in availableActions and not recursive):
            availableActions = availableActions + (square.getRightUpDiagonal().getPosition(),)

    return availableActions


actions(state)