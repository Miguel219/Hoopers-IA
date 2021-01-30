from numpy import * 
from collections import namedtuple

from Square import Square
from Piece import Piece

#Tupla para las coordenadas del tablero
Coord = namedtuple('Coord',['x','y'])

class Game:
    def __init__(self, dimension = 10):
        #Tamaño del tablero
        self.dimension = dimension
        
        #tablero
        self.board = array([[None] * dimension] * dimension) 
        #Jugador 1
        self.player1 = None
        #Jugador 2
        self.player2 = None

        #Llenamos el tablero
        self.fillBoard(dimension)
        #Creamos los movimientos permitidos en las casillas
        self.setAllowedMovements()

    #Crea las casillas y fichas de los jugadores y las coloca en las casillas correspondientes
    def fillBoard(self, dimension):
        #Calculo de piezas por jugador
        numberOfPieces = 0
        while(dimension > 0):
            numberOfPieces += int(dimension/2)
            dimension -= 2

        #Jugador 1
        self.player1 = array([None] * numberOfPieces)
        #Jugador 2
        self.player2 = array([None] * numberOfPieces)

        placedPiecesPlayer1 = 0
        placedPiecesPlayer2 = 0
        #Se llena el tablero 
        for y in range(self.dimension):          
            for x in range(self.dimension):
                if (x + y < (self.dimension/2) or x + y >= ((self.dimension/2) + self.dimension - 1)):
                    if (x + y < (self.dimension/2)):
                        newPiece = Piece(id='1-'+ str(placedPiecesPlayer1 + 1),position=Coord(x + 1,y + 1))
                        self.player1[placedPiecesPlayer1] = newPiece
                        self.board[y][x] = Square(position=Coord(x + 1,y + 1),visitor=newPiece)
                        placedPiecesPlayer1 += 1
                    else:
                        newPiece = Piece(id='2-'+ str(placedPiecesPlayer2 + 1),position=Coord(x + 1,y + 1))
                        self.player2[placedPiecesPlayer2] = newPiece
                        self.board[y][x] = Square(position=Coord(x + 1,y + 1),visitor=newPiece)
                        placedPiecesPlayer2 += 1
                else:
                    self.board[y][x] = Square(position=Coord(x + 1,y + 1))


    #Crea las relaciones entre las casillas 
    def setAllowedMovements(self):

        for row in self.board:
            for square in row:
                currentX, currentY = square.getPosition().x - 1, square.getPosition().y - 1
                #Se crean los movimientos
                if (currentX >= 1):
                    square.setLeft(self.board[currentY][currentX - 1])
                if (currentX <= self.dimension - 2):
                    square.setRight(self.board[currentY][currentX + 1])
                if (currentY <= self.dimension - 2):
                    square.setDown(self.board[currentY + 1][currentX])   
                if (currentY >= 1):
                    square.setUp(self.board[currentY - 1][currentX]) 
                if (currentX >= 1 and currentY <= self.dimension - 2):
                    square.setLeftDownDiagonal(self.board[currentY + 1][currentX - 1])
                if (currentX <= self.dimension - 2 and currentY <= self.dimension - 2):
                    square.setRightDownDiagonal(self.board[currentY + 1][currentX + 1])
                if (currentX >= 1 and currentY >= 1):
                    square.setLeftUpDiagonal(self.board[currentY - 1][currentX - 1])
                if (currentX <= self.dimension - 2  and currentY >= 1):
                    square.setRightUpDiagonal(self.board[currentY - 1][currentX + 1])

                #Se crean los saltos
                if (currentX > 1):
                    square.setHopLeft(self.board[currentY][currentX - 2])
                if (currentX < self.dimension - 2):
                    square.setHopRight(self.board[currentY][currentX + 2])
                if (currentY < self.dimension - 2):
                    square.setHopDown(self.board[currentY + 2][currentX])    
                if (currentY > 1):
                    square.setHopUp(self.board[currentY - 2][currentX])
                if (currentX > 1 and currentY < self.dimension - 2):
                    square.setHopLeftDownDiagonal(self.board[currentY + 2][currentX - 2])
                if (currentX < self.dimension - 2 and currentY < self.dimension - 2):
                    square.setHopRightDownDiagonal(self.board[currentY + 2][currentX + 2])
                if (currentX > 1 and currentY > 1):
                    square.setHopLeftUpDiagonal(self.board[currentY - 2][currentX - 2])
                if (currentX < self.dimension - 2  and currentY > 1):
                    square.setHopRightUpDiagonal(self.board[currentY - 2][currentX + 2])
    
    #Funcion que encuentra un camino de una casilla a otra casilla
    def moveToPath(self, player, initialCoord, finalCoord):
        path = pathForSquareToFinalCoord(self.board[initialCoord.y - 1][initialCoord.x - 1], finalCoord)
        if (path):
            #Se cambia la posición de la pieza del jugador
            for piece in player:
                if (piece.getPosition() == initialCoord):
                    piece.setPosition(finalCoord)
                    #Se cambia la posición de la pieza en el tablero
                    self.board[initialCoord.y - 1][initialCoord.x - 1].setVisitor(None)
                    self.board[finalCoord.y - 1][finalCoord.x - 1].setVisitor(piece)

            return (initialCoord, *path)


#Funcion que devuelve una tupla de las casillas a las que se puede mover una casilla
def squaresToMove(initialCoord, square, availableActions, recursive = False):
    #Revisa movimiento y salto a la izquierda
    if (square.getLeft()):
        if (square.getLeft().visitor):
            if (square.getHopLeft() and square.getHopLeft().visitor is None and (initialCoord, square.getHopLeft().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopLeft().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopLeft(), availableActions, recursive=True)
        elif((initialCoord, square.getLeft().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getLeft().getPosition()))

    #Revisa movimiento y salto a la derecha
    if (square.getRight()):
        if (square.getRight().visitor):
            if (square.getHopRight() and square.getHopRight().visitor is None and (initialCoord, square.getHopRight().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopRight().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopRight(), availableActions, recursive=True)
        elif((initialCoord, square.getRight().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getRight().getPosition()))

    #Revisa movimiento y salto hacia abajo
    if (square.getDown()):
        if (square.getDown().visitor):
            if (square.getHopDown() and square.getHopDown().visitor is None and (initialCoord, square.getHopDown().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopDown().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopDown(), availableActions, recursive=True)
        elif((initialCoord, square.getDown().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getDown().getPosition()))

    #Revisa movimiento y salto hacia arriba
    if (square.getUp()):
        if (square.getUp().visitor):
            if (square.getHopUp() and square.getHopUp().visitor is None and (initialCoord, square.getHopUp().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopUp().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopUp(), availableActions, recursive=True)
        elif((initialCoord, square.getUp().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getUp().getPosition()))

    #Revisa movimiento y salto hacia la diagonal izquierda abajo
    if (square.getLeftDownDiagonal()):
        if (square.getLeftDownDiagonal().visitor):
            if (square.getHopLeftDownDiagonal() and square.getHopLeftDownDiagonal().visitor is None and (initialCoord, square.getHopLeftDownDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopLeftDownDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopLeftDownDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getLeftDownDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getLeftDownDiagonal().getPosition()))

    #Revisa movimiento y salto hacia la diagonal derecha abajo
    if (square.getRightDownDiagonal()):
        if (square.getRightDownDiagonal().visitor):
            if (square.getHopRightDownDiagonal() and square.getHopRightDownDiagonal().visitor is None and (initialCoord, square.getHopRightDownDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopRightDownDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopRightDownDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getRightDownDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getRightDownDiagonal().getPosition()))

    #Revisa movimiento y salto hacia la diagonal izquierda arriba
    if (square.getLeftUpDiagonal()):
        if (square.getLeftUpDiagonal().visitor):
            if (square.getHopLeftUpDiagonal() and square.getHopLeftUpDiagonal().visitor is None and (initialCoord, square.getHopLeftUpDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopLeftUpDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopLeftUpDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getLeftUpDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getLeftUpDiagonal().getPosition()))

    #Revisa movimiento y salto hacia la diagonal derecha arriba
    if (square.getRightUpDiagonal()):
        if (square.getRightUpDiagonal().visitor):
            if (square.getHopRightUpDiagonal() and square.getHopRightUpDiagonal().visitor is None and (initialCoord, square.getHopRightUpDiagonal().getPosition()) not in availableActions):
                availableActions = (*availableActions,(initialCoord, square.getHopRightUpDiagonal().getPosition()))
                availableActions = squaresToMove(initialCoord, square.getHopRightUpDiagonal(), availableActions, recursive=True)
        elif((initialCoord, square.getRightUpDiagonal().getPosition()) not in availableActions and not recursive):
            availableActions = (*availableActions,(initialCoord, square.getRightUpDiagonal().getPosition()))

    return availableActions


#Funcion que devuelve una tupla de el camino de una casilla a otra casilla
def pathForSquareToFinalCoord(square, finalCoord, recursive = False):
    #Revisa movimiento y salto a la izquierda
    if (square.getLeft()):
        if (square.getLeft().visitor):
            if (square.getHopLeft() and square.getHopLeft().visitor is None):
                if (square.getHopLeft().getPosition() == finalCoord):
                    return (square.getHopLeft().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopLeft(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopLeft().getPosition(), *path)
        elif(not recursive):
            if (square.getLeft().getPosition() == finalCoord):
                    return (square.getLeft().getPosition(),)

    #Revisa movimiento y salto a la derecha
    if (square.getRight()):
        if (square.getRight().visitor):
            if (square.getHopRight() and square.getHopRight().visitor is None):
                if (square.getHopRight().getPosition() == finalCoord):
                    return (square.getHopRight().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopRight(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopRight().getPosition(), *path)
        elif(not recursive):
            if (square.getRight().getPosition() == finalCoord):
                    return (square.getRight().getPosition(),)

    #Revisa movimiento y salto hacia abajo
    if (square.getDown()):
        if (square.getDown().visitor):
            if (square.getHopDown() and square.getHopDown().visitor is None):
                if (square.getHopDown().getPosition() == finalCoord):
                    return (square.getHopDown().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopDown(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopDown().getPosition(), *path)
        elif(not recursive):
            if (square.getDown().getPosition() == finalCoord):
                    return (square.getDown().getPosition(),)

    #Revisa movimiento y salto hacia arriba
    if (square.getUp()):
        if (square.getUp().visitor):
            if (square.getHopUp() and square.getHopUp().visitor is None):
                if (square.getHopUp().getPosition() == finalCoord):
                    return (square.getHopUp().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopUp(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopUp().getPosition(), *path)
        elif(not recursive):
            if (square.getUp().getPosition() == finalCoord):
                    return (square.getUp().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal izquierda abajo
    if (square.getLeftDownDiagonal()):
        if (square.getLeftDownDiagonal().visitor):
            if (square.getHopLeftDownDiagonal() and square.getHopLeftDownDiagonal().visitor is None):
                if (square.getHopLeftDownDiagonal().getPosition() == finalCoord):
                    return (square.getHopLeftDownDiagonal().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopLeftDownDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopLeftDownDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getLeftDownDiagonal().getPosition() == finalCoord):
                    return (square.getLeftDownDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal derecha abajo
    if (square.getRightDownDiagonal()):
        if (square.getRightDownDiagonal().visitor):
            if (square.getHopRightDownDiagonal() and square.getHopRightDownDiagonal().visitor is None):
                if (square.getHopRightDownDiagonal().getPosition() == finalCoord):
                    return (square.getHopRightDownDiagonal().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopRightDownDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopRightDownDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getRightDownDiagonal().getPosition() == finalCoord):
                    return (square.getRightDownDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal izquierda arriba
    if (square.getLeftUpDiagonal()):
        if (square.getLeftUpDiagonal().visitor):
            if (square.getHopLeftUpDiagonal() and square.getHopLeftUpDiagonal().visitor is None):
                if (square.getHopLeftUpDiagonal().getPosition() == finalCoord):
                    return (square.getHopLeftUpDiagonal().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopLeftUpDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopLeftUpDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getLeftUpDiagonal().getPosition() == finalCoord):
                    return (square.getLeftUpDiagonal().getPosition(),)

    #Revisa movimiento y salto hacia la diagonal derecha arriba
    if (square.getRightUpDiagonal()):
        if (square.getRightUpDiagonal().visitor):
            if (square.getHopRightUpDiagonal() and square.getHopRightUpDiagonal().visitor is None):
                if (square.getHopRightUpDiagonal().getPosition() == finalCoord):
                    return (square.getHopRightUpDiagonal().getPosition(),)
                else:
                    path = pathForSquareToFinalCoord(square.getHopRightUpDiagonal(), finalCoord, recursive=True)
                    if (path):
                        return (square.getHopRightUpDiagonal().getPosition(), *path)
        elif(not recursive):
            if (square.getRightUpDiagonal().getPosition() == finalCoord):
                    return (square.getRightUpDiagonal().getPosition(),)

    return None